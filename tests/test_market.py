import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_market_requires_authentication():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.get(
            "/market/?coin_id=bitcoin"
        )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_market_requires_filter():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.get(
            "/market/",
            headers={
                "Authorization": "Bearer vetty-dev-key-2026",
            },
        )

    assert response.status_code == 422
@pytest.mark.asyncio
async def test_market_success():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.get(
            "/market/?coin_id=bitcoin",
            headers={
                "Authorization": "Bearer vetty-dev-key-2026",
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["page_num"] == 1
    assert data["per_page"] == 10
    assert "market_data" in data
    assert isinstance(data["market_data"], list)
@pytest.mark.asyncio
async def test_market_pagination():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.get(
            "/market/?coin_id=bitcoin&page_num=1&per_page=5",
            headers={
                "Authorization": "Bearer vetty-dev-key-2026",
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["page_num"] == 1
    assert data["per_page"] == 5
    assert len(data["market_data"]) <= 5
@pytest.mark.asyncio
async def test_market_invalid_per_page():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.get(
            "/market/?coin_id=bitcoin&per_page=101",
            headers={
                "Authorization": "Bearer vetty-dev-key-2026",
            },
        )

    assert response.status_code == 422