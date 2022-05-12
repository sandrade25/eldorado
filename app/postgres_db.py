"""
high level database variables
"""


from functools import cached_property

from pynamodb.exceptions import DoesNotExist
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from alembic import command, config
from app.dynamo.database_connection import DatabaseConnection
from app.settings import BASE_DIR

Base = declarative_base()


class DatabaseUtils:
    @staticmethod
    def get_db_data(schema):
        try:
            return DatabaseConnection.get(schema)
        except DoesNotExist:
            raise

    @staticmethod
    def db_url(username: str, password: str, host: str, port: str, db_name: str = ""):
        return f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}"

    @staticmethod
    def get_alembic_config(
        db_model: DatabaseConnection = None,
        skip_schema: bool = False,
        modded: bool = True,
    ):
        _config = config.Config(f"{BASE_DIR}/app/alembic.ini")
        if not modded:
            return _config

        if not db_model:
            raise Exception

        _config.set_main_option(
            "sqlalchemy.url",
            DatabaseUtils.db_url(
                username=db_model.username,
                password=db_model.password,
                host=db_model.host,
                port=db_model.port,
            ),
        )
        if not skip_schema:
            _config.attributes["schema"] = db_model.schema
        else:
            _config.attributes["schema"] = "public"

        return _config

    @staticmethod
    def create_revision(schema: str, message: str):
        db_model = DatabaseConnection.get(schema)
        _config = DatabaseUtils.get_alembic_config(db_model=db_model)

        command.revision(config=_config, message=message, autogenerate=True)

    @staticmethod
    def upgrade_db(schema: str, revision: str = "head") -> None:
        db_model = DatabaseConnection.get(schema)
        db_model.maintenance = True
        db_model.save()

        _config = DatabaseUtils.get_alembic_config(db_model=db_model)

        command.upgrade(_config, revision)
        db_model.maintenance = False
        db_model.save()


class DatabaseSession:
    def __init__(self, schema: str, force_connection: bool = False, public_schema: bool = False):
        self.utils = DatabaseUtils
        self.schema = schema if not public_schema else "public"

        if not force_connection and self.db_data.maintenance:
            raise Exception

        self.engine, self.session = self._connect_db()
        self.execute = self.session.execute
        self.add = self.session.add
        self.delete = self.session.delete
        self.rollback = self.session.rollback

    def __del__(self):
        self.execute = None
        self.add = None
        self.delete = None
        self.rollback = None
        self.session.close()
        self.engine.dispose()

    def add_new_schema(self, db_model: DatabaseConnection = None):
        if not db_model:
            db_model = DatabaseConnection(
                username=self.db_data.username,
                password=self.db_data.password,
                host=self.db_data.host,
                port=self.db_data.port,
                db_name=self.db_data.db_name,
            )

        db_model.save()
        with self.engine.begin() as connection:
            _config = self.utils.get_alembic_config(db_model=db_model)
            _config.attributes["connection"] = connection
            command.upgrade(_config, "head")

    @cached_property
    def db_data(self):
        return self.utils.get_db_data(schema=self.schema)

    @cached_property
    def db_url(self):
        return self.utils.db_url(
            username=self.db_data.username,
            password=self.db_data.password,
            host=self.db_data.host,
            port=self.db_data.port,
            db_name=self.db_data.db_name,
        )

    def _connect_db(self):
        try:
            engine = create_engine(
                self.db_url, connect_args={"options": "-csearch_path={}".format(self.schema)}
            )
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            session = SessionLocal()
            metadata = MetaData(bind=self.engine)
            metadata.create_all(engine)
            return engine, session
        except (DoesNotExist, AttributeError, ValueError):
            raise
