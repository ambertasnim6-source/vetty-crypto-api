from typing import Annotated

from fastapi import APIRouter, Depends, Query
from app.schemas.coins import CoinListResponse
from app.dependencies import verify_api_key
from app.services.coingecko import CoinGeckoClient


router = APIRouter(prefix="/coins", tags=["Coins"])


@router.get("/",response_model=CoinListResponse)
async def list_coins(
    page_num: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=100)] = 10,
    _: str = Depends(verify_api_key),
):
    client = CoinGeckoClient()

    coins = await client.get_coins(
        page_num=page_num,
        per_page=per_page,
    )

    return {
        "page_num": page_num,
        "per_page": per_page,
        "coins": coins,
    }