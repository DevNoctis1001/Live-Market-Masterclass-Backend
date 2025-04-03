from django.apps import AppConfig
from .utils.telegrambot import TelegramBot
import os

class AlertsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.alerts'

    # def ready(self):
    #     # Import here to avoid circular imports

    #     # Get the to
    #     # kien from the environment variable
    #     token = os.getenv('TELEGRAM_TOKEN')
    #     print(f"Token: {token}")
    #     if not TelegramBot.get_instance():
    #         telegram_bot = TelegramBot(token)
    #     else: 
    #         telegram_bot = TelegramBot.get_instance()
            
    #     telegram_bot.start_bot()