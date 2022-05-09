"""
high level database variables
"""
from sqlalchemy.ext.declarative import declarative_base

from alembic import command, config, script
from app.dynamo.database_connection import DatabaseConnection
from app.settings import BASE_DIR

Base = declarative_base()


class DatabaseUtils:
    # @staticmethod
    # def get_db(db_connection: DatabaseConnection):
    #     from app.postgres_db import DatabaseSession

    #     return DatabaseSession(db_connection.db_identifier)

    @staticmethod
    def db_url(username: str, password: str, host: str, port: str):
        return f"postgresql+psycopg2://{username}:{password}@{host}:{port}"

    @staticmethod
    def create_revision(db_code: str, message: str):
        _config = config.Config(f"{BASE_DIR}/app/alembic.ini")

        db_model = DatabaseConnection.get(db_code)

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
    def upgrade_db(db_code: str, revision: str = "head") -> None:
        db_model = DatabaseConnection.get(db_code)
        db_model.maintainence = True
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
        db_model.maintainence = False
        db_model.save()


class DatabaseSession:
    def __init__(self, db_identifier: str):
        self.utils = DatabaseUtils
