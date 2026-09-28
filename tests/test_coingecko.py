import httpx
import pytest
from unittest.mock import AsyncMock

from app.exceptions.errors import AppException
from app.services.coingecko import CoinGeckoClient


def make_response(data, status_code=200):
    response = httpx.Response(
        status_code,
        json=data,
        request=httpx.Request(
            "GET",
            "https://test.example.com",
        ),
    )
    return response


@pytest.mark.asyncio
async def test_get_coins():
    client = CoinGeckoClient()

    response = make_response(
        [{"id": "bitcoin", "name": "Bitcoin", "symbol": "btc"}]
    )

    client._get = AsyncMock(return_value=response)

    result = await client.get_coins(
        page_num=1,
        per_page=10,
    )

    assert result[0]["id"] == "bitcoin"


@pytest.mark.asyncio
async def test_get_categories():
    client = CoinGeckoClient()

    response = make_response(
        [{"category_id": "layer-1", "name": "Layer 1"}]
    )

    client._get = AsyncMock(return_value=response)

    result = await client.get_categories()

    assert result[0]["category_id"] == "layer-1"


@pytest.mark.asyncio
async def test_get_market_data_from_cache():
    client = CoinGeckoClient()

    cached_data = [
        {
            "id": "bitcoin",
            "current_price": 100000,
        }
    ]

    client.cache.set(
        "market:bitcoin:None:1:10",
        cached_data,
    )

    client._get = AsyncMock()

    result = await client.get_market_data(
        coin_id="bitcoin",
        page_num=1,
        per_page=10,
    )

    assert result == cached_data
    client._get.assert_not_called()


@pytest.mark.asyncio
async def test_market_data_empty_coin_result():
    client = CoinGeckoClient()

    response = make_response([])

    client._get = AsyncMock(return_value=response)

    result = await client.get_market_data(
        coin_id="unknown-coin",
        category="layer-1",
    )

    assert result == []


@pytest.mark.asyncio
async def test_market_data_category_does_not_match_coin():
    client = CoinGeckoClient()

    market_response = make_response(
        [{"id": "bitcoin", "current_price": 100000}]
    )

    coin_response = make_response(
        {
            "id": "bitcoin",
            "categories": ["Cryptocurrency"],
        }
    )

    categories_response = make_response(
        [
            {
                "category_id": "meme-token",
                "name": "Meme",
            }
        ]
    )

    client._get = AsyncMock(
        side_effect=[
            market_response,
            coin_response,
            categories_response,
        ]
    )

    result = await client.get_market_data(
        coin_id="bitcoin",
        category="meme-token",
    )

    assert result == []


@pytest.mark.asyncio
async def test_market_data_page_greater_than_one():
    client = CoinGeckoClient()

    market_response = make_response(
        [{"id": "bitcoin", "current_price": 100000}]
    )

    coin_response = make_response(
        {
            "id": "bitcoin",
            "categories": ["Layer 1"],
        }
    )

    categories_response = make_response(
        [
            {
                "category_id": "layer-1",
                "name": "Layer 1",
            }
        ]
    )

    client._get = AsyncMock(
        side_effect=[
            market_response,
            coin_response,
            categories_response,
        ]
    )

    result = await client.get_market_data(
        coin_id="bitcoin",
        category="layer-1",
        page_num=2,
        per_page=10,
    )

    assert result == []


@pytest.mark.asyncio
async def test_get_handles_timeout():
    client = CoinGeckoClient()

    request = httpx.Request(
        "GET",
        "https://test.example.com",
    )

    client_mock = AsyncMock()

    client_mock.get.side_effect = httpx.TimeoutException(
        "timeout",
        request=request,
    )

    with pytest.raises(AppException) as exc_info:
        await client._get(
            client_mock,
            "https://test.example.com",
        )

    assert exc_info.value.code == "EXTERNAL_SERVICE_TIMEOUT"
    assert exc_info.value.status_code == 504


@pytest.mark.asyncio
async def test_get_handles_http_error():
    client = CoinGeckoClient()

    request = httpx.Request(
        "GET",
        "https://test.example.com",
    )

    response = httpx.Response(
        500,
        request=request,
    )

    client_mock = AsyncMock()
    client_mock.get.return_value = response

    with pytest.raises(AppException) as exc_info:
        await client._get(
            client_mock,
            "https://test.example.com",
        )

    assert exc_info.value.code == "EXTERNAL_SERVICE_ERROR"
    assert exc_info.value.status_code == 503


@pytest.mark.asyncio
async def test_get_handles_request_error():
    client = CoinGeckoClient()

    request = httpx.Request(
        "GET",
        "https://test.example.com",
    )

    client_mock = AsyncMock()

    client_mock.get.side_effect = httpx.ConnectError(
        "connection failed",
        request=request,
    )

    with pytest.raises(AppException) as exc_info:
        await client._get(
            client_mock,
            "https://test.example.com",
        )

    assert exc_info.value.code == "EXTERNAL_SERVICE_UNAVAILABLE"
    assert exc_info.value.status_code == 503