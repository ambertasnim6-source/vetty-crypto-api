from fastapi import FastAPI

from app.api.health import router as health_router
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="REST API for cryptocurrency market data.",
)

app.include_router(health_router)


@app.get("/")
async def root():
    return {
        "message": "Vetty Crypto API is running",
        "version": settings.app_version,
        "environment": settings.environment,
    }