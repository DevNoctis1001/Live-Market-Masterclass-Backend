from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# If modifying these scopes, delete the file token.json.

from .utils.telegrambot import TelegramBot
from .utils.sendnotification import send_telegram_notification

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
def sms_webhook(request):
    if request.method == 'POST':
        try:
            data= json.loads(request.body)
            sms_message = data.get('body')
            sender = data.get('from')
            timestamp = data.get('timestamp')

            print(f"Received SMS: {sms_message} from {sender} at {timestamp}")

            return JsonResponse({'status': 'success'},status = 200)
        except Exception as e:
            print(f"Error processing SMS: {e}")
            return JsonResponse({'status': 'error'}, status=500)
    else:
            return JsonResponse({'message': 'Invalid request method'}, status=405)


@api_view(['GET'])
def main(request):
    print("Start Fetching...")
    print("Creating Telegram Bot...") 
    # return {'ok'}
    # telegram_bot = TelegramBot.get_instance()
    # bot_thread = threading.Thread(target=start_TGbot, daemon=True)
    # bot_thread.start()
    telegram_bot = TelegramBot("7598620067:AAFMSpKJaxZ4gyXCyLW78vi5n5ivuC1b_zM")
    telegram_bot.start_bot()
    return HttpResponse("Telegram bot is running")
#    while True:
      
    # Fetch(telegram_bot)

