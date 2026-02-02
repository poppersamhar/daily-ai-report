from sqlalchemy import Column, String, Text, Integer, DateTime, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(String(255), primary_key=True)  # module_originalId
    module = Column(String(50), nullable=False, index=True)
    title = Column(Text, nullable=False)
    title_zh = Column(Text, default="")
    summary = Column(Text, default="")
    link = Column(String(2048), nullable=False)
    source = Column(String(255), default="")
    author = Column(String(255), default="")
    pub_date = Column(DateTime(timezone=True))
    thumbnail = Column(String(2048), default="")
    tags = Column(JSONB, default=list)
    fame_score = Column(Integer, default=0)
    extra = Column(JSONB, default=dict)
    core_insight = Column(Text, default="")
    key_points = Column(JSONB, default=list)
    is_hero = Column(Integer, default=0)
    fetch_run_id = Column(String(36))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        Index("ix_items_module_fame", "module", fame_score.desc()),
        Index("ix_items_module_hero", "module", "is_hero"),
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "module": self.module,
            "title": self.title,
            "title_zh": self.title_zh,
            "summary": self.summary,
            "link": self.link,
            "source": self.source,
            "author": self.author,
            "pub_date": self.pub_date.isoformat() if self.pub_date else "",
            "thumbnail": self.thumbnail,
            "tags": self.tags or [],
            "fame_score": self.fame_score,
            "extra": self.extra or {},
            "core_insight": self.core_insight,
            "key_points": self.key_points or [],
            "is_hero": self.is_hero,
        }
