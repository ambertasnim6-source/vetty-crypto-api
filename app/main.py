from fastapi import FastAPI
from fastapi import Depends
from app.dependencies import verify_api_key
from app.api.coins import router as coins_router
from app.api.health import router as health_router
from app.config import get_settings
from app.api.categories import router as categories_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="REST API for cryptocurrency market data.",
)

app.include_router(health_router)
app.include_router(coins_router)
app.include_router(categories_router)
@app.get("/")
async def root(_: str = Depends(verify_api_key)):
    return {
        "message": "Vetty Crypto API is running",
        "version": settings.app_version,
        "environment": settings.environment,
    }