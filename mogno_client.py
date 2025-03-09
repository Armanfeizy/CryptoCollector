from pymongo import MongoClient

from util.singleton import Singleton



class MongoHandler(metaclass=Singleton):

    def __init__(self, host: str = "localhost", port: int = 27017, db_name: str = "cryptoCollector"):
        self._client = MongoClient(f"mongodb://{host}:{port}/")
        self._db = self._client[db_name]



