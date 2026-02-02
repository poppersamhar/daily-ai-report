from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database import Base


class FetchRun(Base):
    __tablename__ = "fetch_runs"

    id = Column(String(36), primary_key=True)
    status = Column(String(20), default="pending")  # pending, running, completed, failed
    modules_processed = Column(JSONB, default=dict)
    total_items = Column(Integer, default=0)
    errors = Column(JSONB, default=list)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "status": self.status,
            "modules_processed": self.modules_processed or {},
            "total_items": self.total_items,
            "errors": self.errors or [],
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
