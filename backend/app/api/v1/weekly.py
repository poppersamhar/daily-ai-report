from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.api.deps import get_database
from app.config import get_settings
from app.services.weekly_summary_service import (
    generate_weekly_summary,
    get_latest_weekly_summary,
)

router = APIRouter()


@router.get("/summary")
def get_weekly_summary(db: Session = Depends(get_database)):
    """Get the latest weekly summary"""
    summary = get_latest_weekly_summary(db)
    if not summary:
        return {"error": "No weekly summary available", "data": None}
    return {"data": summary.to_dict()}


@router.post("/summary/generate")
def trigger_weekly_summary(
    db: Session = Depends(get_database),
    x_admin_key: str = Header(None),
):
    """Generate a new weekly summary (requires admin key)"""
    settings = get_settings()
    if x_admin_key != settings.admin_api_key:
        raise HTTPException(status_code=401, detail="Invalid admin key")

    summary = generate_weekly_summary(db)
    if not summary:
        raise HTTPException(status_code=500, detail="Failed to generate weekly summary")

    return {"message": "Weekly summary generated", "data": summary.to_dict()}
