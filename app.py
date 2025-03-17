from datetime import datetime, timezone

import uvicorn
from fastapi import FastAPI

import config
from mogno_client import MongoHandler
from util.public_dto import Timeframe

app = FastAPI(title="CryptoCollector")
mongo_handler = MongoHandler(host=config.MONGO_HOST, port=config.MONGO_PORT)


@app.post("/ohlc/{symbol}")
def fetch_ohlc(symbol: str,
               timeframe: Timeframe,
               start_time: datetime,
               end_time: datetime = datetime.now(tz=timezone.utc)):

    price_data = mongo_handler.fetch_records(symbol, start_time=start_time, end_time=end_time)
    bucket_size = timeframe.get_timedelta()

    # Process OHLC data
    ohlc_buckets = {}

    for record in price_data:
        ts = record["timestamp"]
        bucket_key = ts.replace(
            minute=(ts.minute // bucket_size.seconds * 60) if bucket_size.seconds < 3600 else 0,
            second=0,
            microsecond=0
        )
        if bucket_size.seconds >= 3600:
            bucket_key = bucket_key.replace(
                hour=(ts.hour // (bucket_size.seconds // 3600) * (bucket_size.seconds // 3600)))

        if bucket_key not in ohlc_buckets:
            ohlc_buckets[bucket_key] = {
                "open": record["price"],
                "high": record["price"],
                "low": record["price"],
                "close": record["price"],
                "timestamp": bucket_key
            }
        else:
            ohlc_buckets[bucket_key]["high"] = max(ohlc_buckets[bucket_key]["high"], record["price"])
            ohlc_buckets[bucket_key]["low"] = min(ohlc_buckets[bucket_key]["low"], record["price"])
            ohlc_buckets[bucket_key]["close"] = record["price"]

    return list(ohlc_buckets.values())


if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=7070)