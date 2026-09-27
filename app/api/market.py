from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import verify_api_key
from app.schemas.market import MarketDataResponse
from app.services.coingecko import CoinGeckoClient


router = APIRouter(prefix="/market", tags=["Market Data"])


@router.get("/", response_model=MarketDataResponse)
async def get_market_data(
    coin_id: Annotated[str | None, Query(min_length=1)] = None,
    category: Annotated[str | None, Query(min_length=1)] = None,
    page_num: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=100)] = 10,
    _: str = Depends(verify_api_key),
):
    if not coin_id and not category:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one of coin_id or category is required",
        )

    client = CoinGeckoClient()

    market_data = await client.get_market_data(
        coin_id=coin_id,
        category=category,
        page_num=page_num,
        per_page=per_page,
    )

    return {
        "page_num": page_num,
        "per_page": per_page,
        "market_data": market_data,
    }