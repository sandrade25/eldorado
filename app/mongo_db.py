"""
high level mongodb variables
"""
from ctypes import Union
from functools import cached_property
import sys, os
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.database import Database as mongoDatabase
from pymongo.collection import Collection as mongoCollection
from typing import Any, Dict


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app.settings import MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASSWORD



class MongoUtils:
    @staticmethod
    def mongo_url(username:str, password:str, host:str, port:str):
        return f"mongodb://{username}:{password}@{host}:{port}/"


class MongoCollection:
    def __init__(self, collection: mongoCollection):
        self.collection = collection

    # def __getattribute__(self, __name: str) -> Any:
    #     if __name not in ["collection"]:
    #         try:
    #             self.collections[__name]
    #         except KeyError:
    #             raise AttributeError
    #         else:
    #             if not self.collections[__name]:
    #                 self.collections[__name] = MongoCollection(collection=self.db[__name])
    #             return self.collections[__name]
    #     else:
    #         return super().__getattribute__(__name)

class MongoDB:

    def __init__(self, mongo_client: pymongo.MongoClient, db_name: str):
        self.db_name = db_name
        self.db = mongo_client[self.db_name]

        self.collections: Dict[str, Union[MongoCollection, None]] = {collection_name: None for collection_name in self.db.list_collection_names()}

    def __getattribute__(self, __name: str) -> Any:
        if __name in ["db_name", "db", "collections"]:
            return super(MongoDB, self).__getattribute__(__name)
        else:
            try:
                self.collections[__name]
            except KeyError:
                raise AttributeError
            else:
                if not self.collections[__name]:
                    self.collections[__name] = MongoCollection(collection=self.db[__name])
                return self.collections[__name]


class MongoSession():
    def __init__(self):
        self.utils = MongoUtils
        self.client = pymongo.MongoClient(self.utils.mongo_url(username=MONGO_USER, password=MONGO_PASSWORD, host=MONGO_HOST, port=MONGO_PORT))

        self.dbs: Dict[str, Union[MongoDB, None]] = {db_name: None for db_name in self.client.list_database_names() if db_name not in ["admin", "config", "local"]}

    @property
    def admin(self):
        return self.client["admin"]

    @property
    def config(self):
        return  self.client["config"]

    @property
    def local(self):
        return self.client["local"]

    def __getattribute__(self, __name: str) -> Any:
        if __name in ["utils", "client", "dbs", "admin", "config", "local"]:
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


