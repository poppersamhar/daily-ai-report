from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timedelta

from app.api.deps import get_database
from app.models.item import Item
from app.schemas import ModulesResponse, ModuleInfo, ModuleDetailResponse, ItemResponse

router = APIRouter()

# Module metadata
MODULE_META = {
    "youtube": {"name_zh": "YouTube", "icon": ""},
    "twitter": {"name_zh": "X", "icon": ""},
    "reddit": {"name_zh": "Reddit", "icon": "🔴"},
    "substack": {"name_zh": "Substack", "icon": ""},
    "products": {"name_zh": "开源项目", "icon": ""},
    "business": {"name_zh": "产品及商业", "icon": ""},
    "apple_podcast": {"name_zh": "中文播客", "icon": "🎧"},
}


def item_to_response(item: Item) -> ItemResponse:
    return ItemResponse(
        id=item.id,
        module=item.module,
        title=item.title,
        title_zh=item.title_zh or "",
        summary=item.summary or "",
        link=item.link,
        source=item.source or "",
        author=item.author or "",
        pub_date=item.pub_date.isoformat() if item.pub_date else "",
        thumbnail=item.thumbnail or "",
        tags=item.tags or [],
        fame_score=item.fame_score or 0,
        extra=item.extra or {},
        core_insight=item.core_insight or "",
        key_points=item.key_points or [],
        is_hero=item.is_hero or 0,
    )


@router.get("/", response_model=ModulesResponse)
def get_all_modules(db: Session = Depends(get_database)):
    """Get homepage data with all module previews"""
    today = datetime.now().strftime("%Y-%m-%d")
    modules = []

    for module_name, meta in MODULE_META.items():
        # Get hero item
        hero_item = db.query(Item).filter(
            Item.module == module_name,
            Item.is_hero == 1
        ).first()

        # Get other items (excluding hero)
        query = db.query(Item).filter(Item.module == module_name)
        if hero_item:
            query = query.filter(Item.id != hero_item.id)
        items = query.order_by(desc(Item.fame_score)).limit(3).all()

        total = db.query(Item).filter(Item.module == module_name).count()

        modules.append(ModuleInfo(
            module=module_name,
            module_zh=meta["name_zh"],
            icon=meta["icon"],
            hero=item_to_response(hero_item) if hero_item else None,
            items=[item_to_response(i) for i in items],
            total=total,
        ))

    return ModulesResponse(date=today, modules=modules)


@router.get("/{module}", response_model=ModuleDetailResponse)
def get_module_detail(
    module: str,
    days: int = Query(default=7, ge=1, le=30, description="Filter items from last N days"),
    db: Session = Depends(get_database),
):
    """Get module detail page data with optional date filtering"""
    if module not in MODULE_META:
        return ModuleDetailResponse(
            module=module,
            module_zh=module,
            icon="📄",
            hero=None,
            items=[],
            total=0,
        )

    meta = MODULE_META[module]
    cutoff = datetime.now() - timedelta(days=days)

    # 不需要日期过滤的模块（GitHub Trending 没有明确发布日期）
    skip_date_filter = module in ("products",)

    # Get hero item
    # Twitter/X、Podcast、YouTube、Reddit 选最新的作为 hero，其他模块用 is_hero 标记
    if module in ("twitter", "apple_podcast", "youtube", "reddit"):
        hero_item = db.query(Item).filter(
            Item.module == module,
            Item.pub_date >= cutoff
        ).order_by(desc(Item.pub_date)).first()
    else:
        hero_item = db.query(Item).filter(
            Item.module == module,
            Item.is_hero == 1
        ).first()

    # Get all items (excluding hero)
    query = db.query(Item).filter(Item.module == module)
    if not skip_date_filter:
        query = query.filter(Item.pub_date >= cutoff)
    if hero_item:
        query = query.filter(Item.id != hero_item.id)

    # Twitter/X、Podcast、YouTube、Reddit 按时间排序，其他模块按分数排序
    if module in ("twitter", "apple_podcast", "youtube", "reddit"):
        items = query.order_by(desc(Item.pub_date)).limit(30).all()
    else:
        items = query.order_by(desc(Item.fame_score)).limit(30).all()

    # 计算总数
    total_query = db.query(Item).filter(Item.module == module)
    if not skip_date_filter:
        total_query = total_query.filter(Item.pub_date >= cutoff)
    total = total_query.count()

    return ModuleDetailResponse(
        module=module,
        module_zh=meta["name_zh"],
        icon=meta["icon"],
        hero=item_to_response(hero_item) if hero_item else None,
        items=[item_to_response(i) for i in items],
        total=total,
    )
