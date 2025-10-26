"""Utility helpers for interacting with the database layer."""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from typing import Optional

import redis
from sqlalchemy.orm import Session

from ...config.settings import get_settings
from ...models import User

settings = get_settings()
redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_user_by_telegram_id(db: Session, telegram_id: str) -> Optional[User]:
    """Return a user by Telegram identifier if one exists."""

    return db.query(User).filter(User.telegram_id == telegram_id).first()


def create_user(db: Session, telegram_id: str, **kwargs) -> User:
    """Create a new user entity and persist it immediately."""

    user = User(id=str(uuid.uuid4()), telegram_id=telegram_id, **kwargs)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User, **kwargs) -> User:
    """Update user information and persist the changes."""

    for key, value in kwargs.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def get_or_create_user(db: Session, telegram_id: str, **kwargs) -> User:
    """Return an existing user or create a new one."""

    user = get_user_by_telegram_id(db, telegram_id)
    if not user:
        return create_user(db, telegram_id, **kwargs)

    user.last_interaction = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user


def set_user_cache(user_id: str, data: dict) -> None:
    """Set user data in cache for one hour."""

    redis_client.setex(f"user:{user_id}", 3600, json.dumps(data))


def get_user_cache(user_id: str) -> Optional[dict]:
    """Retrieve cached user data if available."""

    data = redis_client.get(f"user:{user_id}")
    if data:
        return json.loads(data)
    return None


def clear_user_cache(user_id: str) -> None:
    """Remove cached user data."""

    redis_client.delete(f"user:{user_id}")