from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Get main keyboard with three buttons"""
    keyboard = [
        [KeyboardButton("📱 Приложение")],
        [KeyboardButton("🤝 Поддержка")],
        [KeyboardButton("📰 Новости")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

def get_app_keyboard() -> InlineKeyboardMarkup:
    """Get application keyboard"""
    keyboard = [
        [InlineKeyboardButton("🌐 Открыть веб-приложение", url="https://soulmine.app")],
        [InlineKeyboardButton("📱 Открыть Mini App", web_app={"url": "https://soulmine.app/mini-app"})],
        [InlineKeyboardButton("🔗 Привязать кошелёк", callback_data="link_wallet")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_support_keyboard() -> InlineKeyboardMarkup:
    """Get support keyboard"""
    keyboard = [
        [InlineKeyboardButton("💬 Написать в поддержку", url=f"tg://resolve?domain=soulmine_support")],
        [InlineKeyboardButton("📧 Отправить письмо", callback_data="send_email")],
        [InlineKeyboardButton("📞 Звонок в поддержку", callback_data="call_support")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_news_keyboard() -> InlineKeyboardMarkup:
    """Get news keyboard"""
    keyboard = [
        [InlineKeyboardButton("📢 Последние новости", callback_data="latest_news")],
        [InlineKeyboardButton("🔔 Включить уведомления", callback_data="enable_notifications")],
        [InlineKeyboardButton("🔕 Выключить уведомления", callback_data="disable_notifications")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_to_main_keyboard() -> InlineKeyboardMarkup:
    """Get back to main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)