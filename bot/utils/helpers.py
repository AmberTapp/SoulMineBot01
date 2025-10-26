"""Generic helper functions used across the bot."""

from __future__ import annotations

import re
import uuid

from ...config.settings import get_settings

settings = get_settings()


def generate_referral_code(user_id: str) -> str:
    """Generate a short referral code based on user id."""

    return f"REF-{user_id[:8].upper()}-{str(uuid.uuid4())[:4].upper()}"


def validate_telegram_username(username: str) -> bool:
    """Validate Telegram username format."""

    if len(username) < 5 or len(username) > 32:
        return False
    pattern = r"^[a-zA-Z0-9_]+$"
    return re.match(pattern, username) is not None


def validate_wallet_address(address: str) -> bool:
    """Validate TON wallet address."""

    return len(address) == 48 and address.startswith("UQ")


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format currency amount."""

    if currency == "USD":
        return f"${amount:,.2f}"
    if currency == "TON":
        return f"{amount:.9f} TON"
    if currency == "LOVE":
        return f"{amount:.9f} $LOVE"
    return f"{amount:.2f} {currency}"


def get_user_level(level: int) -> str:
    """Get user level name."""

    levels = {
        1: "Новичок",
        2: "Активный",
        3: "Эксперт",
        4: "Легенда",
        5: "Божество",
    }
    return levels.get(level, "Неизвестный")


def is_admin(user_id: int) -> bool:
    """Check if user is admin."""

    return user_id in settings.ADMIN_IDS