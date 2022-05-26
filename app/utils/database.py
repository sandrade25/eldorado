from alembic import command, config
from app.dynamo.database_connection import DatabaseConnection
from app.settings import BASE_DIR
from pynamodb.exceptions import DoesNotExist
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DatabaseUtils:
    @staticmethod
    def get_db_data(db_schema):
        try:
            return DatabaseConnection.get(db_schema)
        except DoesNotExist:
            raise

    @staticmethod
    def db_url(username: str, password: str, host: str, port: str, db_name: str = ""):
        return f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}"

    @staticmethod
    def get_alembic_config(
        db_model: DatabaseConnection = None,
        skip_db_schema: bool = False,
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
                db_name=db_model.db_name,
            ),
        )
        if not skip_db_schema:
            _config.attributes["db_schema"] = db_model.db_schema
        else:
            _config.attributes["db_schema"] = "public"

        return _config

    @staticmethod
    def create_revision(db_model, message: str):
        _config = DatabaseUtils.get_alembic_config(db_model=db_model)

        command.revision(config=_config, message=message, autogenerate=True)

    @staticmethod
    def upgrade_db(db_model, revision: str = "head") -> None:
        db_model.maintenance = True
        db_model.save()

        _config = DatabaseUtils.get_alembic_config(db_model=db_model)

        command.upgrade(_config, revision)
        db_model.maintenance = False
        db_model.save()
