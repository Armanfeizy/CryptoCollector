import logging
from datetime import datetime
from typing import Optional, Union, Dict, List

import requests
from requests import Response

from candlestick.candle import Candle
from candlestick.chart import Chart
from util.public_dto import Timeframe
from util.visualizer import plot_combined

logger = logging.getLogger(__name__)

class JsonResponse:

    def __init__(self, response: Response):
        self.status_code = response.status_code
        self.data: dict = response.json()


class BinanceWrapper:

    BASE_URL = "https://api.binance.com/api/v3"

    @staticmethod
    def get_symbols() -> Optional[list[str]]:
        data = BinanceWrapper.exchange_info()
        return [symbol["symbol"] for symbol in data.get("symbols", [])] if data else None

    @staticmethod
    def get_top_24h_pairs(base_currency: str = None, length: int = 50) -> list[str]:
        json_response = BinanceWrapper._request_to_binance(path="/ticker/24hr")

        pairs = [pair for pair in json_response.data if base_currency is None or pair["symbol"].endswith(base_currency)]

        pairs = sorted(pairs, key=lambda x: float(x["quoteVolume"]), reverse=True)

        if length:
            pairs = pairs[:length]

        return [pair["symbol"] for pair in pairs]


    @staticmethod
    def fetch_price(symbol: str | list[str]) -> Optional[dict[str, float]]:
        is_list = isinstance(symbol, list)

        if is_list:
            params = {"symbols": json.dumps(symbol, separators=(",", ":"))}
        else:
            params = {"symbol": symbol}

        json_response = BinanceWrapper._request_to_binance(path="/ticker/price", params=params)
        if json_response is None:
            return None

        if is_list:
            price_data = json_response.data
        else:
            price_data = [json_response.data]

        return {p_data.get("symbol"): float(p_data.get("price")) for p_data in price_data}

    @staticmethod
    def fetch_candles(symbol: str, timeframe: Timeframe, start_time: Optional[datetime] = None,
                      end_time: Optional[datetime] = None, limit: int = 500) -> Optional[List[Dict[str, Union[float, int]]]]:
        """
        Fetch OHLCV (candlestick) data for a given symbol and timeframe.

        :param symbol: Trading pair symbol (e.g., "BTCUSDT")
        :param timeframe: Time interval (e.g., "1m", "5m", "1h", "1d")
        :param start_time: (Optional) Filter for start time (datetime object)
        :param end_time: (Optional) Filter for end time (datetime object)
        :param limit: Number of candles to fetch (default: 500, max: 1000)
        :return: List of OHLCV data
        """
        params = {
            "symbol": symbol,
            "interval": timeframe.value,
            "limit": limit
        }

        if start_time:
            params["startTime"] = int(start_time.timestamp() * 1000)  # Convert to milliseconds
        if end_time:
            params["endTime"] = int(end_time.timestamp() * 1000)  # Convert to milliseconds

        json_response = BinanceWrapper._request_to_binance(path="/klines", params=params)

        if json_response is None:
            return None

        # Process Binance response into structured OHLCV format
        candles = [
            {
                "timestamp": candle[0],  # Open time (milliseconds)
                "open": float(candle[1]),  # Open price
                "high": float(candle[2]),  # High price
                "low": float(candle[3]),  # Low price
                "close": float(candle[4]),  # Close price
                "volume": float(candle[5]),  # Volume
                "close_time": candle[6],  # Close time (milliseconds)
                "quote_asset_volume": float(candle[7]),  # Quote asset volume
                "trades": int(candle[8]),  # Number of trades
                "taker_buy_base": float(candle[9]),  # Taker buy base asset volume
                "taker_buy_quote": float(candle[10]),  # Taker buy quote asset volume
            }
            for candle in json_response.data
        ]

        return candles


    @staticmethod
    def exchange_info() -> Optional[dict]:
        path = "/exchangeInfo"
        json_response = BinanceWrapper._request_to_binance(path=path)
        return json_response.data if json_response else None

    @staticmethod
    def _build_url(path: str) -> str:
        if path.startswith("/api/v3"):
            path = path.removeprefix("/api/v3")
        if not path.startswith("/"):
            path = "/" + path

        return BinanceWrapper.BASE_URL + path

    @staticmethod
    def _request_to_binance(path: str, method: str = "get", *args, **kwargs) -> Optional[JsonResponse]:
        url = BinanceWrapper._build_url(path)
        try:
            response = requests.request(method, url, *args, **kwargs)
            response.raise_for_status()
            return JsonResponse(response)
        except Exception as e:
            logger.error(e, exc_info=True)
            return None



if __name__ == '__main__':
    symbol = "BTCUSDT"
    timeframe = Timeframe.FIFTEEN_MINUTES
    # res = BinanceWrapper.fetch_candles(symbol, timeframe=timeframe, limit=100)
    import json
    with open("static/sample_candle_data_btcusdt.json", "r") as f:
        res = json.load(f)

    candles = []
    for c in res:
        candles.append(Candle(**c))

    chart = Chart(candles=candles)

    # swings_chart = chart.get_swings_as_chart()

    plot_combined(chart, symbol, num_buckets=40)
    # price_counts = detect_price_reactions(res)
    # plot_heatmap(price_counts)
    # plot_ohlc(res, symbol, timeframe)

    # print(res)

