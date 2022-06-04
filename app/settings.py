import configparser
import os
import sys

from passlib.context import CryptContext

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

config = configparser.ConfigParser()

if os.path.exists(f"{BASE_DIR}/app/conf/app.ini"):
    config.read(f"{BASE_DIR}/app/conf/app.ini")
else:
    if not os.path.exists(f"{BASE_DIR}/app/conf/app_local.ini"):
        raise FileNotFoundError()
    config.read(f"{BASE_DIR}/app/conf/app_local.ini")


ENVIRONMENT = config.get("APPLICATION VARIABLES", "ENVIRONMENT")

DYNAMO_HOST = config.get("DYNAMO", "DYNAMO_HOST")
DYNAMO_PORT = config.get("DYNAMO", "DYNAMO_PORT")

POSTGRES_HOST = config.get("POSTGRES", "POSTGRES_HOST")
POSTGRES_PORT = config.get("POSTGRES", "POSTGRES_PORT")
POSTGRES_USER = config.get("POSTGRES", "POSTGRES_USER")
POSTGRES_PASSWORD = config.get("POSTGRES", "POSTGRES_PASSWORD")

MONGO_HOST = config.get("MONGO", "MONGO_HOST")
MONGO_PORT = config.get("MONGO", "MONGO_PORT")
MONGO_USER = config.get("MONGO", "MONGO_USER")
MONGO_PASSWORD = config.get("MONGO", "MONGO_PASSWORD")

HASH_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SIGNATURE = config.get("APP AUTH", "JWT_SIGNATURE")
JWT_ALGORITHM = "HS256"
JWT_TOKEN_EXPIRATION = 30
