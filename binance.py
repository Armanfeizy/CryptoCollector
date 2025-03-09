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
        json_response = BinanceWrapper._request_to_binance(path="/exchangeInfo")
        return [symbol["symbol"] for symbol in json_response.data.get("symbols", [])] if json_response else None

    @staticmethod
    def fetch_price(symbol: str) -> Optional[float]:
        json_response = BinanceWrapper._request_to_binance(path="/ticker/price", params={"symbol": symbol})
        if json_response is None or json_response.data.get("price", None) is None:
            return None
        return float(json_response.data.get("price"))


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


