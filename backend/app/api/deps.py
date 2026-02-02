from typing import Generator
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import get_settings, Settings


def get_database() -> Generator[Session, None, None]:
    yield from get_db()


def get_config() -> Settings:
    return get_settings()


def verify_admin_key(
    x_admin_key: str = Header(..., alias="X-Admin-Key"),
    settings: Settings = Depends(get_config)
) -> bool:
    if x_admin_key != settings.admin_api_key:
        raise HTTPException(status_code=403, detail="Invalid admin key")
    return True
