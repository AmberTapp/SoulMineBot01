"""Handlers for news-related actions."""

from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import ContextTypes

from ...config.database import get_db
from ..keyboards.main_keyboard import get_back_to_main_keyboard, get_news_keyboard
from ..utils.database import get_user_by_telegram_id

logger = logging.getLogger(__name__)

async def handle_news_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle News button"""
    user = update.effective_user
    with get_db() as db:
        user_obj = get_user_by_telegram_id(db, str(user.id))
    
    if not user_obj:
        await update.message.reply_text("Пожалуйста, сначала зарегистрируйтесь, используя команду /start")
        return
    
    # Send news options
    news_message = (
        "📰 *Новости SoulMine*\n\n"
        "Оставайтесь в курсе последних событий:\n\n"
        "• 📢 Последние новости - важные обновления\n"
        "• 🔔 Включить уведомления - получайте оповещения\n"
        "• 🔕 Выключить уведомления - отключите нотификации\n\n"
        "Что вы хотите сделать?"
    )
    
    await update.message.reply_text(news_message, reply_markup=get_news_keyboard(), parse_mode="Markdown")

async def latest_news_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle latest news callback"""
    query = update.callback_query
    await query.answer()
    
    # Send latest news
    news_message = (
        "📢 *Последние новости*\n\n"
        "🎉 *Объявляем запуск нового сезона!* (20.10.2024)\n\n"
        "Сегодня мы запускаем новый сезон с увеличенными наградами и новыми функциями:\n"
        "• Увеличена награда за майнинг $LOVE токенов на 20%\n"
        "• Добавлены новые NFT коллекции\n"
        "• Улучшен алгоритм подбора пар\n"
        "• Добавлена возможность видеозвонков\n\n"
        "Спасибо, что вы с нами! 🎉"
    )
    
    await query.edit_message_text(news_message, reply_markup=get_back_to_main_keyboard(), parse_mode="Markdown")

async def enable_notifications_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle enable notifications callback"""
    query = update.callback_query
    await query.answer()
    
    # Enable notifications
    user = update.effective_user
    with get_db() as db:
        user_obj = get_user_by_telegram_id(db, str(user.id))

        if user_obj:
            user_obj.notifications_enabled = True
            db.commit()

            # Send confirmation
            confirm_message = (
                "🔔 *Уведомления включены*\n\n"
                "Теперь вы будете получать уведомления о:\n"
                "• Новых сообщениях\n"
                "• Новых матчах\n"
                "• Наградах за активность\n"
                "• Акциях и событиях\n\n"
                "Вы всегда можете отключить уведомления, нажав соответствующую кнопку."
            )

            await query.edit_message_text(confirm_message, reply_markup=get_back_to_main_keyboard(), parse_mode="Markdown")
        else:
            await query.edit_message_text("Произошла ошибка. Попробуйте снова.", reply_markup=get_back_to_main_keyboard())

async def disable_notifications_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle disable notifications callback"""
    query = update.callback_query
    await query.answer()
    
    # Disable notifications
    user = update.effective_user
    with get_db() as db:
        user_obj = get_user_by_telegram_id(db, str(user.id))

        if user_obj:
            user_obj.notifications_enabled = False
            db.commit()

            # Send confirmation
            confirm_message = (
                "🔕 *Уведомления отключены*\n\n"
                "Вы больше не будете получать уведомления.\n\n"
                "Вы всегда можете включить их обратно, нажав соответствующую кнопку."
            )

            await query.edit_message_text(confirm_message, reply_markup=get_back_to_main_keyboard(), parse_mode="Markdown")
        else:
            await query.edit_message_text("Произошла ошибка. Попробуйте снова.", reply_markup=get_back_to_main_keyboard())