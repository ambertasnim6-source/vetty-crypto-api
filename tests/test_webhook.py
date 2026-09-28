import httpx

from app.services import webhook


class FakeClient:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        return None

    async def post(self, url, json):
        return None


class FailingClient:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        return None

    async def post(self, url, json):
        raise httpx.RequestError("Webhook request failed")


def test_webhook_skips_when_url_not_configured(monkeypatch):
    class Settings:
        webhook_url = ""
        request_timeout = 10.0

    monkeypatch.setattr(
        webhook,
        "get_settings",
        lambda: Settings(),
    )

    import asyncio

    asyncio.run(
        webhook.send_webhook(
            {"event": "market_data_retrieved"}
        )
    )


def test_webhook_sends_successfully(monkeypatch):
    class Settings:
        webhook_url = "https://example.com/webhook"
        request_timeout = 10.0

    monkeypatch.setattr(
        webhook,
        "get_settings",
        lambda: Settings(),
    )

    monkeypatch.setattr(
        webhook.httpx,
        "AsyncClient",
        lambda timeout: FakeClient(),
    )

    import asyncio

    asyncio.run(
        webhook.send_webhook(
            {"event": "market_data_retrieved"}
        )
    )


def test_webhook_handles_request_error(monkeypatch):
    class Settings:
        webhook_url = "https://example.com/webhook"
        request_timeout = 10.0

    monkeypatch.setattr(
        webhook,
        "get_settings",
        lambda: Settings(),
    )

    monkeypatch.setattr(
        webhook.httpx,
        "AsyncClient",
        lambda timeout: FailingClient(),
    )

    import asyncio

    asyncio.run(
        webhook.send_webhook(
            {"event": "market_data_retrieved"}
        )
    )