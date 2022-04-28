"""
high level database variables
"""
import sys, os
from sqlalchemy.ext.declarative import declarative_base
from alembic import command, config, script

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

Base = declarative_base()

def create_revision(message:str):
    _config = config.Config(f"{BASE_DIR}/app/alembic.ini")
    command.revision(config=_config, message=message, autogenerate=True)


if __name__ == "__main__": 
    create_revision("first migration test")