from typing import List, Callable

import numpy as np
import pandas as pd
from candlestick.candle import Candle


class Chart:

    def __init__(self, candles: list[Candle] | list[dict]):
        if len(candles) == 0:
            raise ValueError("Chart can no be empty")

        if isinstance(candles[0], Candle):
            self.candles = candles
        else:
            self.candles = [Candle(**c) for c in candles]

    def get_swings(self) -> List[Candle]:
        return [Candle.get_swing_candle(self.candles[i], self.candles[i + 1]) for i in range(len(self.candles) - 1)
                if Candle.is_swing(self.candles[i], self.candles[i + 1])]

    def get_swings_as_chart(self) -> 'Chart':
        return Chart(candles=self.get_swings())

    def get_min_value(self):
        if hasattr(self, "_min"):
            return self._min

        min_value = min(c.low for c in self.candles)
        object.__setattr__(self, "_min", min_value)
        return min_value

    def get_max_value(self):
        if hasattr(self, "_max"):
            return self._max

        max_value = max(c.high for c in self.candles)
        object.__setattr__(self, "_max", max_value)
        return max_value

    def get_as_data_frame(self, use_cache: bool = True) -> pd.DataFrame:
        if use_cache and hasattr(self, "_df"):
            return self._df

        df = pd.DataFrame([c.to_dict() for c in self.candles])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)

        # Rename columns to match mplfinance format
        df = df[["open", "high", "low", "close", "volume"]]

        object.__setattr__(self, "_df", df)
        return df

    def get_price_buckets(self, num_buckets: int) -> list[float]:
        return np.linspace(self.get_min_value(), self.get_max_value(), num_buckets).flatten().tolist()

    def get_swing_prices(self, value_fetcher: Callable[[Candle], float] = None) -> list[float]:
        if value_fetcher is None:
            value_fetcher = lambda c: c.high
        return [value_fetcher(c) for c in self.get_swings()]

