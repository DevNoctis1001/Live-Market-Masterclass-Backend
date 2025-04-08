from .telegrambot1 import TelegramBot

def send_telegram_notification(message):
    """
    Send a notification via Telegram bot
    """
    bot= TelegramBot.get_instance()

    if bot:
        return bot.notify(message)
    return False