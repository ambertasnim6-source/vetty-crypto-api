import logging

import httpx

from app.cache.memory import InMemoryCache
from app.config import get_settings
from app.exceptions.errors import AppException
from app.services.webhook import send_webhook

logger = logging.getLogger(__name__)


class CoinGeckoClient:
    def __init__(self):
        self.settings = get_settings()
        self.cache = InMemoryCache(ttl=self.settings.cache_ttl)
    async def _get(self, client, url, params=None):
        try:
            response = await client.get(
                url,
                params=params,
            )
            response.raise_for_status()
            return response

        except httpx.TimeoutException as exc:
            raise AppException(
                code="EXTERNAL_SERVICE_TIMEOUT",
                message="CoinGecko request timed out",
                status_code=504,
            ) from exc

        except httpx.HTTPStatusError as exc:
            raise AppException(
                code="EXTERNAL_SERVICE_ERROR",
                message="CoinGecko service returned an error",
                status_code=503,
            ) from exc

        except httpx.RequestError as exc:
            raise AppException(
                code="EXTERNAL_SERVICE_UNAVAILABLE",
                message="Unable to connect to CoinGecko",
                status_code=503,
            ) from exc

    async def get_coins(self, page_num: int = 1, per_page: int = 10):
        params = {
            "vs_currency": "cad",
            "per_page": per_page,
            "page": page_num,
        }

        async with httpx.AsyncClient(
            timeout=self.settings.request_timeout
        ) as client:
            response = await self._get(
                client,
                f"{self.settings.coingecko_base_url}/coins/markets",
                params=params,
            )


            return response.json()

    async def get_categories(self):
        async with httpx.AsyncClient(
            timeout=self.settings.request_timeout
        ) as client:
            response = await self._get(
                client,
                f"{self.settings.coingecko_base_url}/coins/categories/list"
            )

            return response.json()
    async def get_market_data(
        self,
        coin_id: str | None = None,
        category: str | None = None,
        page_num: int = 1,
        per_page: int = 10,
    ):
        cache_key = (
            f"market:{coin_id}:{category}:"
            f"{page_num}:{per_page}"
        )

        cached_data = self.cache.get(cache_key)

        if cached_data is not None:
            logger.info("Market data served from cache",)
            return cached_data

        async with httpx.AsyncClient(
            timeout=self.settings.request_timeout
        ) as client:

            if coin_id and category:
                market_response = await self._get(
                    client,
                    f"{self.settings.coingecko_base_url}/coins/markets",
                    params={
                        "vs_currency": "cad",
                        "ids": coin_id,
                        "per_page": 1,
                        "page": 1,
                    },
                )
                market_response.raise_for_status()
                market_data = market_response.json()

                if not market_data:
                    return []

                coin_response = await self._get(
                    client,
                    f"{self.settings.coingecko_base_url}/coins/{coin_id}"
                )
                coin_details = coin_response.json()

                coin_categories = coin_details.get("categories", [])

                categories_response = await self._get(
                    client,
                    f"{self.settings.coingecko_base_url}/coins/categories/list"
                )
                categories_response.raise_for_status()
                categories = categories_response.json()

                category_name = next(
                    (
                        item["name"]
                        for item in categories
                        if item.get("category_id") == category
                    ),
                    None,
                )

                if category_name not in coin_categories:
                    self.cache.set(cache_key, [])
                    return []
                if page_num>1:
                    return []

                result= market_data[:per_page]
                self.cache.set(cache_key, result)
                await send_webhook(
                    {
                        "event": "market_data_retrieved",
                        "coin_id": coin_id,
                        "category": category,
                        "page_num": page_num,
                        "per_page": per_page,
                        "market_data": result,
                    }
                )
                return result

            params = {
                "vs_currency": "cad",
                "per_page": per_page,
                "page": page_num,
            }

            if coin_id:
                params["ids"] = coin_id

            if category:
                params["category"] = category

            response = await self._get(
                client,
                f"{self.settings.coingecko_base_url}/coins/markets",
                params=params,
            )

            market_data = response.json()

            self.cache.set(cache_key, market_data)
            await send_webhook(
                {
                    "event": "market_data_retrieved",
                    "coin_id": coin_id,
                    "category": category,
                    "page_num": page_num,
                    "per_page": per_page,
                    "market_data": market_data,
                }
            )

            return market_data
coingecko_client = CoinGeckoClient()
