"""
high level database variables
"""
import sys, os
from sqlalchemy.ext.declarative import declarative_base
from alembic import command, config, script

from app.settings import BASE_DIR

Base = declarative_base()

class DatabaseUtils:
    @staticmethod
    def db_url(username: str, password:str, host:str, port:str):
        return f"postgresql+psycopg2://{username}:{password}@{host}:{port}"

    @staticmethod
    def create_revision(db_code:str, message:str):
        _config = config.Config(f"{BASE_DIR}/app/alembic.ini")

        # TODO : make mongo model.
        db_model = mongo_model.get(db_code) # code mongo model associated with db_code provided. 

        # overwrite sql alchemy url with database environment url in settings
        _config.set_main_option("sqlalchemy.url", DatabaseUtils.db_url(username=db_model.username, password=db_model.password, host=db_model.host, port=db_model.port))

        command.revision(config=_config, message=message, autogenerate=True)


class DatabaseSession:
    def __init__(self):
        self.utils = DatabaseUtils

    



