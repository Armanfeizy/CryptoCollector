from datetime import datetime, timezone
from pymongo import MongoClient, ASCENDING

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

    def fetch_records(self, symbol: str, start_time: datetime = None, end_time: datetime = None) -> list:
        query = {"symbol": symbol}

        time_filter = {}
        if start_time:
            time_filter["$gte"] = start_time
        if end_time:
            time_filter["$lte"] = end_time

        if time_filter:
            query["timestamp"] = time_filter

        # Fetch price data from MongoDB

        price_data = list(self._price_collection.find().sort("timestamp", ASCENDING))
        return price_data if price_data else []



