"""Handlers for the application-related menu."""

from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import ContextTypes

from ...config.database import get_db
from ..keyboards.main_keyboard import (
    get_app_keyboard,
    get_back_to_main_keyboard,
    get_main_keyboard,
)
from ..utils.database import get_user_by_telegram_id

logger = logging.getLogger(__name__)


async def handle_app_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the "Приложение" button from the main menu."""

    user = update.effective_user
    with get_db() as db:
        user_obj = get_user_by_telegram_id(db, str(user.id))

    if not user_obj:
        await update.message.reply_text(
            "Пожалуйста, сначала зарегистрируйтесь, используя команду /start",
        )
        return

    app_message = (
        "📱 *Приложение SoulMine*\n\n"
        "Выберите, как вы хотите использовать приложение:\n\n"
        "• 🌐 Веб-приложение — полная версия на сайте\n"
        "• 📱 Mini App — лёгкая версия в Telegram\n"
        "• 🔗 Привязать кошелёк — для работы с токенами $LOVE\n\n"
        "Что вы хотите сделать?"
    )

    await update.message.reply_text(
        app_message,
        reply_markup=get_app_keyboard(),
        parse_mode="Markdown",
    )


async def link_wallet_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Respond to the «link wallet» callback button."""

    query = update.callback_query
    await query.answer()

    wallet_message = (
        "🔗 *Привязка кошелька*\n\n"
        "Чтобы подключить TON-кошелёк:\n"
        "1. Откройте приложение SoulMine.\n"
        "2. Перейдите в раздел «Кошелёк».\n"
        "3. Следуйте инструкциям на экране или используйте ссылку ниже.\n\n"
        "👉 [Привязать кошелёк](https://soulmine.app/wallet)\n\n"
        "После привязки вы сможете управлять токенами $LOVE и получать награды."
    )

    await query.edit_message_text(
        wallet_message,
        reply_markup=get_back_to_main_keyboard(),
        parse_mode="Markdown",
    )


async def open_web_app_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Respond to the «open web app» callback button."""

    query = update.callback_query
    await query.answer()

    web_app_message = (
        "🌐 *Веб-приложение SoulMine*\n\n"
        "Полная версия доступна в браузере и поддерживает все функции платформы:\n"
        "• Расширенный профиль\n"
        "• Продвинутый поиск\n"
        "• Управление наградами и кошельком\n\n"
        "👉 [Открыть веб-приложение](https://soulmine.app)"
    )

    await query.edit_message_text(
        web_app_message,
        reply_markup=get_back_to_main_keyboard(),
        parse_mode="Markdown",
    )


async def open_mini_app_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Respond to the «open mini app» callback button."""

    query = update.callback_query
    await query.answer()

    mini_app_message = (
        "📱 *Mini App SoulMine*\n\n"
        "Используйте лёгкую версию приложения прямо в Telegram:\n\n"
        "👉 [Открыть Mini App](https://t.me/soulmine_bot?startapp=mini_app)\n\n"
        "Mini App позволяет:\n"
        "• Быстро общаться с пользователями\n"
        "• Получать базовые награды\n"
        "• Просматривать профили\n"
        "• Участвовать в чатах\n\n"
        "Идеально для быстрого использования!"
    )

    await query.edit_message_text(
        mini_app_message,
        reply_markup=get_back_to_main_keyboard(),
        parse_mode="Markdown",
    )


async def back_to_main_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return the user to the main reply keyboard."""

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🏠 *Главное меню*",
        parse_mode="Markdown",
    )

    await query.message.reply_text(
        "Выберите действие из меню ниже:",
        reply_markup=get_main_keyboard(),
    )