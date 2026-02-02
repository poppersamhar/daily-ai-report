from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://localhost/daily_ai_report"

    # API Keys
    deepseek_api_key: str = ""
    rapidapi_key: str = ""
    admin_api_key: str = "changeme"

    # CORS
    frontend_url: str = "http://localhost:5173"

    # Scheduler
    fetch_cron_hour: int = 8  # Run at 8 AM
    fetch_cron_minute: int = 0

    # Fetcher settings
    max_items_per_module: int = 30
    time_window_hours: int = 168  # 7 days

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
