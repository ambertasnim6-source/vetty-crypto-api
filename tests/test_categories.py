import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_categories_requires_authentication():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.get("/categories/")

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_categories_success():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.get(
            "/categories/",
            headers={
                "Authorization": "Bearer vetty-dev-key-2026",
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert "categories" in data
    assert data["page_num"] == 1
    assert data["per_page"] == 10