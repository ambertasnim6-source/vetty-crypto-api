from pydantic import BaseModel


class Coin(BaseModel):
    id: str
    name: str
    symbol: str


class CoinListResponse(BaseModel):
    page_num: int
    per_page: int
    coins: list[Coin]