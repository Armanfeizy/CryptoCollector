import os
import json


###### logging ######
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Logging configuration
LOG_FILE = os.path.join(LOG_DIR, "price_fetcher.log")


###### MONGO CONNECTION SETTINGS ######
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", "27017"))
MONGO_DB = os.getenv("MONGO_DB", "cryptoCollector")


try:
    with open("static/symbols.json") as f:
        SUPPORTED_SYMBOLS: list[str] = json.load(f)
except Exception as e:
    raise ValueError("Failed to load symbols.json")