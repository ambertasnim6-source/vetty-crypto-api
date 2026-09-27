from pydantic import BaseModel


class Category(BaseModel):
    id: str
    name: str


class CategoryListResponse(BaseModel):
    page_num: int
    per_page: int
    categories: list[Category]
    