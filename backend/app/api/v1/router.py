from fastapi import APIRouter
from app.api.v1 import modules, items, admin, weekly

router = APIRouter()

router.include_router(modules.router, prefix="/modules", tags=["modules"])
router.include_router(items.router, prefix="/items", tags=["items"])
router.include_router(admin.router, prefix="/admin", tags=["admin"])
router.include_router(weekly.router, prefix="/weekly", tags=["weekly"])
