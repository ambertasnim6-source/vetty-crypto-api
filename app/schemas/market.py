from pydantic import BaseModel


class MarketData(BaseModel):
    id: str
    symbol: str
    name: str
    current_price: float | None = None
    market_cap: float | None = None
    total_volume: float | None = None
    price_change_percentage_24h: float | None = None


class MarketDataResponse(BaseModel):
    page_num: int
    per_page: int
    market_data: list[MarketData]