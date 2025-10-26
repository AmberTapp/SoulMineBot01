"""Application settings and configuration helpers."""

from __future__ import annotations

from functools import lru_cache
from typing import Iterable, List

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["Settings", "get_settings", "settings"]


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables."""

    TELEGRAM_BOT_TOKEN: str = "TEST_TOKEN"
    DATABASE_URL: str = "sqlite:///./soulmine.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    WEB_APP_URL: AnyHttpUrl = "https://example.com"

    SUPPORT_CHAT_ID: int = 0
    NEWS_CHANNEL_ID: int = 0

    ADMIN_IDS: List[int] = []

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @field_validator("ADMIN_IDS", mode="before")
    @classmethod
    def _parse_admin_ids(cls, value: str | Iterable[int]) -> List[int]:
        """Allow comma separated admin identifiers in environment."""

        if isinstance(value, str):
            if not value.strip():
                return []
            return [int(item.strip()) for item in value.split(",") if item.strip()]

        return [int(item) for item in value]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached :class:`Settings` instance."""

    return Settings()


# Backwards compatibility -----------------------------------------------------

settings = get_settings()