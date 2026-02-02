from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TagSchema(BaseModel):
    label: str
    type: str = "topic"


class ItemBase(BaseModel):
    title: str
    title_zh: str = ""
    summary: str = ""
    link: str
    source: str = ""
    author: str = ""
    thumbnail: str = ""
    tags: list[TagSchema] = []
    fame_score: int = 0
    extra: dict = {}


class ItemCreate(ItemBase):
    id: str
    module: str
    pub_date: Optional[datetime] = None


class ItemResponse(ItemBase):
    id: str
    module: str
    pub_date: str = ""
    core_insight: str = ""
    key_points: list[str] = []
    is_hero: int = 0

    class Config:
        from_attributes = True


class ItemListResponse(BaseModel):
    items: list[ItemResponse]
    total: int
    page: int = 1
    page_size: int = 20
