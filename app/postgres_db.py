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
from app.utils.database import DatabaseUtils


class DatabaseSession:
    def __init__(self, schema: str, force_connection: bool = False, public_schema: bool = False):
        self.utils = DatabaseUtils
        self.schema = schema
        self.db_data
        if public_schema:
            self.schema = "public"

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

    def create_revision(self, message: str):
        db_model = self.db_data
        db_model.schema = self.schema
        self.utils.create_revision(db_model, message)

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

    def _connect_db(self, schema_override: str = None):
        schema = self.schema if not schema_override else schema_override
        try:
            engine = create_engine(
                self.db_url, connect_args={"options": "-csearch_path={}".format(schema)}
            )
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            session = SessionLocal()
            metadata = MetaData(bind=engine)
            metadata.create_all(engine)
            return engine, session
        except (DoesNotExist, AttributeError, ValueError):
            raise
