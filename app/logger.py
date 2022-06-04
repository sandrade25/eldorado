import json
import logging
from logging.config import dictConfig

from app.settings import ENVIRONMENT

with open("/var/www/eldorado/logging.json", "r") as fp:
    dictConfig(json.load(fp))

logger = logging.getLogger(__name__)

if ENVIRONMENT == "local":
    logger.setLevel("DEBUG")
