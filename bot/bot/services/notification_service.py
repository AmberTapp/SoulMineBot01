"""Notification related helper services."""

from __future__ import annotations

import logging
from typing import Dict

from telegram import Bot
from telegram.error import TelegramError

from ...config.database import get_db
from ...models import User

logger = logging.getLogger(__name__)


class NotificationService:
    """Service responsible for sending notifications to Telegram users."""

    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_notification(self, user_id: str, message: str, parse_mode: str | None = None) -> bool:
        """Send notification to a single user."""

        try:
            await self.bot.send_message(chat_id=user_id, text=message, parse_mode=parse_mode)
            return True
        except TelegramError as exc:  # pragma: no cover - network errors
            logger.error("Failed to send notification to %s: %s", user_id, exc)
            return False

    async def broadcast_notification(self, message: str, parse_mode: str | None = None) -> Dict[str, int]:
        """Broadcast notification to all subscribed users."""

        with get_db() as db:
            recipients = db.query(User).filter(User.notifications_enabled.is_(True)).all()

        success_count = 0
        fail_count = 0

        for user in recipients:
            if await self.send_notification(user.telegram_id, message, parse_mode):
                success_count += 1
            else:
                fail_count += 1

        return {
            "total_sent": len(recipients),
            "success_count": success_count,
            "fail_count": fail_count,
        }

    async def send_welcome_notification(self, user_id: str) -> bool:
        """Send welcome notification to new user."""

        message = (
            "👋 Привет! Добро пожаловать в SoulMine!\n\n"
            "Мы рады, что вы с нами. Вот что вы можете сделать:\n"
            "• 📱 Откройте приложение и настройте профиль\n"
            "• 🤝 Начните знакомства с другими пользователями\n"
            "• 💰 Получайте $LOVE токены за активность\n"
            "• 🎁 Получайте награды и достижения\n\n"
            "Удачи в поиске пары!"
        )

        return await self.send_notification(user_id, message)

    async def send_reward_notification(self, user_id: str, reward_amount: float, reward_type: str) -> bool:
        """Send reward notification to user."""

        message = (
            f"🎉 Поздравляем! Вы получили {reward_amount} {reward_type}!\n\n"
            "Спасибо за вашу активность на платформе.\n"
            "Продолжайте в том же духе!"
        )

        return await self.send_notification(user_id, message)

    async def send_match_notification(self, user_id: str, match_user_id: str) -> bool:
        """Send match notification to user."""

        message = (
            "💖 У вас есть новый матч!\n\n"
            "Кто-то из пользователей отметил вас как интересного собеседника.\n"
            "Посмотрите профиль и начните общение!"
        )

        return await self.send_notification(user_id, message)


_notification_service: NotificationService | None = None


def get_notification_service(bot: Bot) -> NotificationService:
    """Return a cached notification service instance."""

    global _notification_service
    if _notification_service is None or _notification_service.bot is not bot:
        _notification_service = NotificationService(bot)
    return _notification_service