import logging
import time

import schedule

import config
from binance import BinanceWrapper
from mogno_client import MongoHandler



logging.basicConfig(
    level=logging.INFO,  # Set log level
    format="%(asctime)s [%(levelname)s] %(message)s",  # Add timestamp & level
    handlers=[
        logging.StreamHandler(),  # Print logs to console
        logging.FileHandler(config.LOG_FILE, mode="a")
    ]
)

logger = logging.getLogger(__name__)


mongo_handler = MongoHandler(host=config.MONGO_HOST, port=config.MONGO_PORT)

def periodic_job():
    logger.info("Start periodic job")

    symbols = ["BTCUSDT", "ETHUSDT"]
    result_dict = BinanceWrapper.fetch_price(symbol=symbols)
    for symbol, price in result_dict.items():
        mongo_handler.insert_price(symbol=symbol, price=price)

    logger.info(f"Successfully insert {len(result_dict)} record to DB")

if __name__ == '__main__':
    periodic_job()
    schedule.every(1).minutes.do(periodic_job)
    while True:
        schedule.run_pending()
        time.sleep(1)

