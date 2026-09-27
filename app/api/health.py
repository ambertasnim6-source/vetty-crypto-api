import httpx
from fastapi import APIRouter

from app.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/health")
async def health_check():
    external_status = "unreachable"

    try:
        async with httpx.AsyncClient(
            timeout=settings.request_timeout
        ) as client:
            response = await client.get(
                f"{settings.coingecko_base_url}/ping"
            )

            if response.is_success:
                external_status = "reachable"

    except (httpx.RequestError, httpx.TimeoutException):
        external_status = "unreachable"

    return {
        "status": "healthy",
        "app_version": settings.app_version,
        "external_service": {
            "name": "CoinGecko",
            "status": external_status,
        },
    }