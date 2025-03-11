from datetime import datetime, timezone
from pymongo import MongoClient

from util.singleton import Singleton



class MongoHandler(metaclass=Singleton):
    PRICE_COLLECTION_NAME = "price"

    def __init__(self, host: str = "localhost", port: int = 27017, db_name: str = "cryptoCollector"):
        self._client = MongoClient(f"mongodb://{host}:{port}/")
        self._db = self._client[db_name]
        self._price_collection = self._db[MongoHandler.PRICE_COLLECTION_NAME]


    def insert_price(self, symbol: str, price: float):
        self._price_collection.insert_one(
            {
                "symbol": symbol,
                "price": price,
                "timestamp": datetime.now(timezone.utc)
            }
        )



