from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Vetty Crypto API"
    app_version: str = "1.0.0"
    environment: str = "development"

    coingecko_base_url: str = "https://api.coingecko.com/api/v3"
    request_timeout: float = 10.0
    cache_ttl: int = 60

    webhook_url: str = ""
    api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()