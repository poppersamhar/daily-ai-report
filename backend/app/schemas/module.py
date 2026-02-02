from pydantic import BaseModel
from typing import Optional
from app.schemas.item import ItemResponse


class ModuleInfo(BaseModel):
    module: str
    module_zh: str
    icon: str
    hero: Optional[ItemResponse] = None
    items: list[ItemResponse] = []
    total: int = 0


class ModulesResponse(BaseModel):
    date: str
    modules: list[ModuleInfo]


class ModuleDetailResponse(BaseModel):
    module: str
    module_zh: str
    icon: str
    hero: Optional[ItemResponse] = None
    items: list[ItemResponse] = []
    total: int = 0
