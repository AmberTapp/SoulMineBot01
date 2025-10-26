"""Telegram update handlers for the SoulMine bot."""

from .app import (
    back_to_main_callback,
    handle_app_button,
    link_wallet_callback,
    open_mini_app_callback,
    open_web_app_callback,
)
from .news import (
    disable_notifications_callback,
    enable_notifications_callback,
    handle_news_button,
    latest_news_callback,
)
from .start import start
from .support import (
    call_support_callback,
    contact_support_callback,
    handle_support_button,
    send_email_callback,
)

__all__ = [
    "back_to_main_callback",
    "handle_app_button",
    "link_wallet_callback",
    "open_mini_app_callback",
    "open_web_app_callback",
    "disable_notifications_callback",
    "enable_notifications_callback",
    "handle_news_button",
    "latest_news_callback",
    "start",
    "call_support_callback",
    "contact_support_callback",
    "handle_support_button",
    "send_email_callback",
]