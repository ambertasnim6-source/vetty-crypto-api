from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.dependencies import verify_api_key
from app.schemas.category import CategoryListResponse
from app.services.coingecko import coingecko_client

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=CategoryListResponse)
async def list_categories(
    page_num: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=100)] = 10,
    _: str = Depends(verify_api_key),
):
    categories = await coingecko_client.get_categories()

    start = (page_num - 1) * per_page
    end = start + per_page

    paginated_categories = categories[start:end]
    formatted_categories = [
        {"id": category["category_id"], "name": category["name"],} for category in paginated_categories]

    return {
        "page_num": page_num,
        "per_page": per_page,
        "categories": formatted_categories,
    }