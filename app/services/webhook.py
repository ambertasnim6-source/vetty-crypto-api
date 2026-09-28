import httpx

from app.config import get_settings


async def send_webhook(payload: dict) -> None:
    settings = get_settings()

    if not settings.webhook_url:
        return

    try:
        async with httpx.AsyncClient(
            timeout=settings.request_timeout
        ) as client:
            await client.post(
                settings.webhook_url,
                json=payload,
            )

    except httpx.RequestError:
        return