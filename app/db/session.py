from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


def _require_db_url() -> str:
    if not settings.database_url:
        raise RuntimeError("DATABASE_URL is not set")
    return settings.database_url


engine = create_engine(_require_db_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
