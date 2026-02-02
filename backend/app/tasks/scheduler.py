from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import uuid

from app.config import get_settings

scheduler = BackgroundScheduler()
settings = get_settings()


def scheduled_fetch():
    """Scheduled fetch job that runs daily"""
    from app.services.fetcher_service import run_fetch_job
    run_id = str(uuid.uuid4())
    print(f"[Scheduler] Starting scheduled fetch: {run_id}")
    run_fetch_job(run_id)


def start_scheduler():
    """Start the background scheduler"""
    # 北京时间早上8点 = UTC 0点
    scheduler.add_job(
        scheduled_fetch,
        CronTrigger(hour=0, minute=0, timezone='UTC'),
        id="daily_fetch",
        replace_existing=True,
    )
    scheduler.start()
    print(f"[Scheduler] Started - daily fetch at 08:00 Beijing Time (00:00 UTC)")


def shutdown_scheduler():
    """Shutdown the scheduler"""
    if scheduler.running:
        scheduler.shutdown()
        print("[Scheduler] Shutdown complete")
