import httpx

from app.config import get_settings


class CoinGeckoClient:
    def __init__(self):
        self.settings = get_settings()

    async def get_coins(self, page_num: int = 1, per_page: int = 10):
        params = {
            "vs_currency": "cad",
            "per_page": per_page,
            "page": page_num,
        }

        async with httpx.AsyncClient(
            timeout=self.settings.request_timeout
        ) as client:
            response = await client.get(
                f"{self.settings.coingecko_base_url}/coins/markets",
                params=params,
            )

            response.raise_for_status()
            return response.json()

    async def get_categories(self):
        async with httpx.AsyncClient(
            timeout=self.settings.request_timeout
        ) as client:
            response = await client.get(
                f"{self.settings.coingecko_base_url}/coins/categories/list"
            )

            response.raise_for_status()
            return response.json()