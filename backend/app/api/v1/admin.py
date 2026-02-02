from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.api.deps import get_database, verify_admin_key
from app.models.fetch_run import FetchRun
from app.services.fetcher_service import run_fetch_job

router = APIRouter()


@router.post("/fetch/trigger")
def trigger_fetch(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_database),
    _: bool = Depends(verify_admin_key),
):
    """Trigger a new fetch job"""
    run_id = str(uuid.uuid4())

    # Create fetch run record
    fetch_run = FetchRun(id=run_id, status="pending")
    db.add(fetch_run)
    db.commit()

    # Run fetch in background
    background_tasks.add_task(run_fetch_job, run_id)

    return {"id": run_id, "status": "pending", "message": "Fetch job started"}


@router.get("/fetch/status/{run_id}")
def get_fetch_status(
    run_id: str,
    db: Session = Depends(get_database),
):
    """Get fetch job status"""
    fetch_run = db.query(FetchRun).filter(FetchRun.id == run_id).first()
    if not fetch_run:
        raise HTTPException(status_code=404, detail="Fetch run not found")
    return fetch_run.to_dict()


@router.get("/fetch/latest")
def get_latest_fetch(db: Session = Depends(get_database)):
    """Get latest fetch run"""
    fetch_run = db.query(FetchRun).order_by(FetchRun.created_at.desc()).first()
    if not fetch_run:
        return {"message": "No fetch runs found"}
    return fetch_run.to_dict()
