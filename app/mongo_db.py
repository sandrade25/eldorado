"""
high level mongodb variables
"""
from ctypes import Union
from functools import cached_property
import sys, os
import pymongo
from pymongo.collection import Collection as mongoCollection
from mongokit import Connection, Document
from typing import Any, Dict


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app.settings import MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASSWORD


class MongoSession():
    def __init__(self):
        self.utils = MongoUtils
        self.connection = Connection(self.utils.mongo_url(username=MONGO_USER, password=MONGO_PASSWORD, host=MONGO_HOST, port=MONGO_PORT))

        self.dbs: Dict[str, Union[MongoDB, None]] = {db_name: None for db_name in self.client.list_database_names() if db_name not in ["admin", "config", "local"]}
        self._register_models()

    @staticmethod
    def mongo_url(username:str, password:str, host:str, port:str):
        return f"mongodb://{username}:{password}@{host}:{port}/"

    @property
    def admin(self):
        return self.connection["admin"]

    @property
    def config(self):
        return  self.connection["config"]

    @property
    def local(self):
        return self.connection["local"]

    def __getattribute__(self, __name: str) -> Any:
        if __name in ["utils", "connection", "dbs", "admin", "config", "local"]:
            return super(MongoSession, self).__getattribute__(__name)
        else:
            try:
                self.dbs[__name]
            except KeyError:
                raise AttributeError
            else:
                if not self.dbs[__name]:
                    self.dbs[__name] = MongoDB(self.client, __name)
                return self.dbs[__name]


    def _register_models(self):
        from app.mongo import mongo_models
        self.connection.register(mongo_models)


