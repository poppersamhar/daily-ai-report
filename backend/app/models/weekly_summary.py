from sqlalchemy import Column, String, Text, Integer, Date, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database import Base


class WeeklySummary(Base):
    __tablename__ = "weekly_summaries"

    id = Column(String(36), primary_key=True)
    week_start = Column(Date, index=True)
    week_end = Column(Date)
    headline = Column(Text, default="")
    hot_topics = Column(JSONB, default=list)
    trend_analysis = Column(Text, default="")
    key_events = Column(JSONB, default=list)
    company_mentions = Column(JSONB, default=dict)
    total_items = Column(Integer, default=0)
    modules_stats = Column(JSONB, default=dict)
    created_at = Column(DateTime, server_default=func.now())

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "week_start": self.week_start.isoformat() if self.week_start else "",
            "week_end": self.week_end.isoformat() if self.week_end else "",
            "headline": self.headline,
            "hot_topics": self.hot_topics or [],
            "trend_analysis": self.trend_analysis,
            "key_events": self.key_events or [],
            "company_mentions": self.company_mentions or {},
            "total_items": self.total_items,
            "modules_stats": self.modules_stats or {},
            "created_at": self.created_at.isoformat() if self.created_at else "",
        }
