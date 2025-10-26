"""Handlers for the /start command."""

from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import ContextTypes

from ...config.database import get_db
from ..keyboards.main_keyboard import get_main_keyboard
from ..utils.database import get_or_create_user
from ..utils.helpers import generate_referral_code

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""

    user = update.effective_user

    with get_db() as db:
        user_obj = get_or_create_user(
            db,
            str(user.id),
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            language_code=user.language_code,
        )

        if not user_obj.referral_code:
            user_obj.referral_code = generate_referral_code(str(user.id))
            db.commit()

    welcome_message = (
        f"👋 Привет, {user.first_name or 'друг'}!\n\n"
        "Добро пожаловать в SoulMine — платформу Web3 знакомств с майнингом $LOVE токенов!\n\n"
        "Выберите действие из меню ниже:"
    )

    await update.message.reply_text(welcome_message, reply_markup=get_main_keyboard())
    logger.info("User %s started the bot", user.id)
