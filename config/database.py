"""Database helpers for the Telegram bot."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .settings import get_settings

__all__ = ["Base", "SessionLocal", "engine", "get_db", "init_db"]


settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
    future=True,
)


class Base(DeclarativeBase):
    """Base class for declarative SQLAlchemy models."""


SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


@contextmanager
def get_db() -> Iterator[Session]:
    """Provide a transactional scope around a series of operations."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create database tables for all models."""

    from ..models import user  # noqa: F401  Import models for metadata registration

    Base.metadata.create_all(bind=engine)