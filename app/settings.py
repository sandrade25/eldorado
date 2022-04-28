import configparser
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app.utils.database import db_url
config = configparser.ConfigParser()





if os.path.exists(f"{BASE_DIR}/app/conf/app.ini"):
    config.read(f"{BASE_DIR}/app/conf/app.ini")
else:
    if not os.path.exists(f"{BASE_DIR}/app/conf/app_local.ini"):
        raise FileNotFoundError()
    config.read(f"{BASE_DIR}/app/conf/app_local.ini")


TEMP_DATABASE_URL = db_url(
        user=config.get("POSTGRES", "USERNAME"), 
        password=config.get("POSTGRES", "PASSWORD"), 
        host=config.get("POSTGRES", "POSTGRES_IP"), 
        port=config.get("POSTGRES", "PORT")
    )

print(TEMP_DATABASE_URL)