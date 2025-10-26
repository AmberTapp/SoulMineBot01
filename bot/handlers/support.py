"""Handlers for support-related actions."""

from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import ContextTypes

from ...config.database import get_db
from ..keyboards.main_keyboard import get_back_to_main_keyboard, get_support_keyboard
from ..utils.database import get_user_by_telegram_id

logger = logging.getLogger(__name__)

async def handle_support_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle Support button"""
    user = update.effective_user
    with get_db() as db:
        user_obj = get_user_by_telegram_id(db, str(user.id))
    
    if not user_obj:
        await update.message.reply_text("Пожалуйста, сначала зарегистрируйтесь, используя команду /start")
        return
    
    # Send support options
    support_message = (
        "🤝 *Поддержка SoulMine*\n\n"
        "Мы здесь, чтобы помочь вам! Выберите способ связи с поддержкой:\n\n"
        "• 💬 Написать в поддержку - быстрый ответ в Telegram\n"
        "• 📧 Отправить письмо - подробный ответ по email\n"
        "• 📞 Звонок в поддержку - если нужно срочно\n\n"
        "Какой способ вам удобнее?"
    )
    
    await update.message.reply_text(support_message, reply_markup=get_support_keyboard(), parse_mode="Markdown")

async def send_email_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle send email callback"""
    query = update.callback_query
    await query.answer()
    
    # Send email instructions
    user = update.effective_user
    email_message = (
        "📧 *Отправить письмо в поддержку*\n\n"
        "Для отправки письма в поддержку:\n"
        "1. Напишите ваш вопрос или проблему\n"
        "2. Укажите ваш Telegram ID: `{user_id}`\n"
        "3. Отправьте письмо на адрес: support@soulmine.app\n\n"
        "Мы ответим вам в течение 24 часов.\n\n"
        "Также вы можете использовать другие способы связи, перечисленные выше."
    ).format(user_id=user.id)
    
    await query.edit_message_text(email_message, reply_markup=get_back_to_main_keyboard(), parse_mode="Markdown")

async def call_support_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle call support callback"""
    query = update.callback_query
    await query.answer()
    
    # Send call support instructions
    call_message = (
        "📞 *Звонок в поддержку*\n\n"
        "Для срочной помощи вы можете позвонить в поддержку:\n\n"
        "☎️ Телефон: +1 (555) 123-4567\n"
        "🕒 Рабочее время: 9:00-21:00 (UTC+3)\n\n"
        "Если вы не можете дозвониться, оставьте сообщение и мы перезвоним вам в течение 30 минут.\n\n"
        "Также доступны другие способы связи, перечисленные выше."
    )
    
    await query.edit_message_text(call_message, reply_markup=get_back_to_main_keyboard(), parse_mode="Markdown")

async def contact_support_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle contact support callback"""
    query = update.callback_query
    await query.answer()
    
    # Send contact support instructions
    contact_message = (
        "💬 *Написать в поддержку*\n\n"
        "Вы можете написать в поддержку прямо сейчас:\n\n"
        "👉 [Написать в поддержку](tg://resolve?domain=soulmine_support)\n\n"
        "Наши операторы ответят вам в течение 15 минут.\n\n"
        "Также доступны другие способы связи, перечисленные выше."
    )
    
    await query.edit_message_text(contact_message, reply_markup=get_back_to_main_keyboard(), parse_mode="Markdown")
