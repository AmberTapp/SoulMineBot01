"""SoulMine Telegram bot package."""

from __future__ import annotations

from importlib import metadata

__all__ = ["__version__"]

try:
    __version__ = metadata.version("soulmine-bot")
except metadata.PackageNotFoundError:  # pragma: no cover - package metadata absent
    __version__ = "5.0.0"