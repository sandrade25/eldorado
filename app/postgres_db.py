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
    def get_db_data(db_id):
        try:
            return DatabaseConnection.get(db_id)
        except DoesNotExist:
            raise

    @staticmethod
    def db_url(username: str, password: str, host: str, port: str):
        return f"postgresql+psycopg2://{username}:{password}@{host}:{port}"

    @staticmethod
    def create_revision(db_id: str, message: str):
        _config = config.Config(f"{BASE_DIR}/app/alembic.ini")

        db_model = DatabaseConnection.get(db_id)

        # overwrite sql alchemy url with database environment url in settings
        _config.set_main_option(
            "sqlalchemy.url",
            DatabaseUtils.db_url(
                username=db_model.username,
                password=db_model.password,
                host=db_model.host,
                port=db_model.port,
            ),
        )

        command.revision(config=_config, message=message, autogenerate=True)

    @staticmethod
    def upgrade_db(db_id: str, revision: str = "head") -> None:
        db_model = DatabaseConnection.get(db_id)
        db_model.maintenance = True
        db_model.save()
        _config = config.Config(f"{BASE_DIR}/app/alembic.ini")

        # db = DatabaseUtils.get_db(db_model)

        # overwrite sql alchemy url with database environment url in settings
        _config.set_main_option(
            "sqlalchemy.url",
            DatabaseUtils.db_url(
                username=db_model.username,
                password=db_model.password,
                host=db_model.host,
                port=db_model.port,
            ),
        )

        command.upgrade(_config, revision)
        db_model.maintenance = False
        db_model.save()


class DatabaseSession:
    def __init__(self, db_id: str, force_connection: bool = False):
        self.utils = DatabaseUtils
        self.db_id = db_id

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

    @cached_property
    def db_data(self):
        return self.utils.get_db_data(db_id=self.db_id)

    @cached_property
    def db_url(self):
        return self.utils.db_url(
            username=self.db_data.username,
            password=self.db_data.password,
            host=self.db_data.host,
            port=self.db_data.port,
        )

    def _connect_db(self):
        try:
            engine = create_engine(self.db_url)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            session = SessionLocal()
            metadata = MetaData(bind=self.engine)
            metadata.create_all(engine)
            return engine, session
        except (DoesNotExist, AttributeError, ValueError):
            raise
