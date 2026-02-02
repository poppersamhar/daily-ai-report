from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_

from app.api.deps import get_database
from app.models.item import Item
from app.schemas import ItemResponse, ItemListResponse
from app.api.v1.modules import item_to_response

router = APIRouter()


@router.get("/", response_model=ItemListResponse)
def search_items(
    q: str = Query(default="", description="Search query"),
    module: str = Query(default="", description="Filter by module"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_database),
):
    """Search items with optional filters"""
    query = db.query(Item)

    if module:
        query = query.filter(Item.module == module)

    if q:
        search_term = f"%{q}%"
        query = query.filter(
            or_(
                Item.title.ilike(search_term),
                Item.title_zh.ilike(search_term),
                Item.summary.ilike(search_term),
                Item.source.ilike(search_term),
            )
        )

    total = query.count()
    items = query.order_by(desc(Item.fame_score)).offset(
        (page - 1) * page_size
    ).limit(page_size).all()

    return ItemListResponse(
        items=[item_to_response(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: str, db: Session = Depends(get_database)):
    """Get single item by ID"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return ItemResponse(
            id=item_id,
            module="",
            title="Not Found",
            link="",
        )
    return item_to_response(item)
