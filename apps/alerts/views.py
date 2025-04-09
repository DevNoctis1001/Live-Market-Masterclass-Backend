from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# If modifying these scopes, delete the file token.json.
import base64 

from .utils.telegrambot import TelegramBot
from .utils.sendnotification import send_telegram_notification

import schedule
import time
from apps.alerts.utils.EmailFetch.setup_gmail_watch import setup_gmail_watch


import json
# def start_TGbot():
#     telegram_bot = TelegramBot.get_instance("7598620067:AAFMSpKJaxZ4gyXCyLW78vi5n5ivuC1b_zM")

#     if telegram_bot and not telegram_bot.application:
#        loop = asyncio.new_event_loop()
#        asyncio.set_event_loop(loop)

#        loop.run_until_complete(telegram_bot.main())

#        # Keep the loop running in a separate thread
        
#     telegram_bot.start_bot()
#     send_telegram_notification("Hello Sending notification")    
#     asyncio.run(telegram_bot.main())

# def send_telegram_notification(message):
#   """Send a notification via Telegram bot"""

#   bot = TelegramBot.get_instance()
#   if bot:
#     return(bot.notify(message))
#   return False

@csrf_exempt
def gmail_webhook(request):
    print(f'request : {request}')
    try:
        message = json.loads(request.body)
        print(f'Received message: {message}')
        if 'message' in message:
            pubsub_message = message['message']
            if 'data' in pubsub_message:
                decoded_data = base64.b64decode(pubsub_message['data']).decode('utf-8')
                data = json.loads(decoded_data)
                print(f'New email notification received: {decoded_data}')
        return HttpResponse(status = 200)
    except Exception as e:
        print(f'Error: {e}')
        return HttpResponse(status = 200)

def renew_watch():
    print("Renewing Gmail watch....")
    setup_gmail_watch()

# Schedule Regualar Watch Renewal
def schedule_renew_watch():
    schedule.every(5).days.do(renew_watch)
    renew_watch()
    while True:
        schedule.run_pending()
        time.sleep(3600) # Check every hour

@api_view(['GET'])
def main(request):
    print("Start Fetching...")
    print("Creating Telegram Bot...") 
    try:
        if TelegramBot.get_instance() == None :
            telegram_bot = TelegramBot("7598620067:AAFMSpKJaxZ4gyXCyLW78vi5n5ivuC1b_zM")
            telegram_bot.start_bot()
    except Exception as e:
        pass
        # print(f"Error creating Telegram bot: {e}")
    # Schedule Regular Watch Renewal
    # schedule_renew_watch()
    return HttpResponse("Telegram bot is running")
