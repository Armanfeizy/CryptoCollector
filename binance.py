import json
import logging
from typing import Optional

import requests
from requests import Response

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




