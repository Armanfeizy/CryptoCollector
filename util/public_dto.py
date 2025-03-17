from datetime import timedelta
from enum import Enum

_TIMEFRAME_MAP = {
        "5m": timedelta(minutes=5),
        "15m": timedelta(minutes=15),
        "30m": timedelta(minutes=30),
        "1h": timedelta(hours=1),
        "4h": timedelta(hours=4),
        "1d": timedelta(days=1),
    }


class Timeframe(Enum):

    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    THIRTY_MINUTES = "30m"

    ONE_HOUR = "1h"
    FOUR_HOURS = "4h"

    ONE_DAY = "1d"

    def get_timedelta(self) -> timedelta:
        return _TIMEFRAME_MAP.get(self.value)
