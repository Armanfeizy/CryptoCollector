from typing import Optional


class Candle:

    def __init__(self, timestamp: int, open: float, high: float, low: float, close: float, volume: float, **kwargs):
        self.timestamp = timestamp
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.kwargs = kwargs

    def to_dict(self) -> dict[str, int | float]:
        return {
            "timestamp": self.timestamp,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
        }

    def is_increasing(self) -> bool:
        return self.open < self.close

    @staticmethod
    def is_swing(o1: 'Candle', o2: 'Candle') -> bool:
        return o1.is_increasing() ^ o2.is_increasing()

    @staticmethod
    def get_swing_candle(o1: 'Candle', o2: 'Candle') -> Optional['Candle']:
        if Candle.is_swing(o1, o2):
            if o1.is_increasing():  # Increase to Decrease
                if o1.high > o2.high:  #swing candle is first one
                    return o1
                else:
                    return o2
            else:  # Decrease to increase
                if o1.low > o2.low:
                    return o1
                else:
                    return o2

        return None