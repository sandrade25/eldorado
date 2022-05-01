import configparser
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

POSTRGES_HOST = config.get("POSTGRES", "POSTRGES_HOST")
POSTGRES_PORT = config.get("POSTGRES", "POSTGRES_PORT")

MONGO_HOST = config.get("MONGO", "MONGO_HOST")
MONGO_PORT = config.get("MONGO", "MONGO_PORT")
MONGO_USER = config.get("MONGO", "MONGO_USER")
MONGO_PASSWORD = config.get("MONGO", "MONGO_PASSWORD")
