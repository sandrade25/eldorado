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


