"""Entry point for the Telegram bot application."""

from __future__ import annotations

import logging
from typing import Final

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from ..config.settings import get_settings
from . import build_application
from .handlers.app import (
    back_to_main_callback,
    handle_app_button,
    link_wallet_callback,
    open_mini_app_callback,
    open_web_app_callback,
)
from .handlers.news import (
    disable_notifications_callback,
    enable_notifications_callback,
    handle_news_button,
    latest_news_callback,
)
from .handlers.start import start
from .handlers.support import (
    call_support_callback,
    contact_support_callback,
    handle_support_button,
    send_email_callback,
)

LOGGER_NAME: Final[str] = "soulmine.bot"


def create_application() -> Application:
    """Create an application instance with all handlers registered."""

    application = build_application()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(MessageHandler(filters.Regex("^📱 Приложение$"), handle_app_button))
    application.add_handler(MessageHandler(filters.Regex("^🤝 Поддержка$"), handle_support_button))
    application.add_handler(MessageHandler(filters.Regex("^📰 Новости$"), handle_news_button))

    application.add_handler(CallbackQueryHandler(link_wallet_callback, pattern="^link_wallet$"))
    application.add_handler(CallbackQueryHandler(open_web_app_callback, pattern="^open_web_app$"))
    application.add_handler(CallbackQueryHandler(open_mini_app_callback, pattern="^open_mini_app$"))
    application.add_handler(CallbackQueryHandler(back_to_main_callback, pattern="^main_menu$"))

    application.add_handler(CallbackQueryHandler(send_email_callback, pattern="^send_email$"))
    application.add_handler(CallbackQueryHandler(call_support_callback, pattern="^call_support$"))
    application.add_handler(CallbackQueryHandler(contact_support_callback, pattern="^contact_support$"))

    application.add_handler(CallbackQueryHandler(latest_news_callback, pattern="^latest_news$"))
    application.add_handler(CallbackQueryHandler(enable_notifications_callback, pattern="^enable_notifications$"))
    application.add_handler(CallbackQueryHandler(disable_notifications_callback, pattern="^disable_notifications$"))

    return application


def main() -> None:
    """Run the Telegram bot."""

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    logger = logging.getLogger(LOGGER_NAME)
    settings = get_settings()
    logger.info("Starting SoulMine bot with webhook URL %s", settings.WEB_APP_URL)

    application = create_application()
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()