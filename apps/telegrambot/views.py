from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TelegramUser, Message
import json
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.telegrambot.credential import TELEGRAM_API_URL

@csrf_exempt
def telegram_bot(request):
    if request.method == "POST" :
        message = json.loads(request.body.decode('utf-8'))
        chat_id = message['message']['chat']['id']
        username = message['message']['chat'].get('username', '')
        text = message['message']['text']
        print(f"chat id:{chat_id}\nusername: {username}\ntext:{text}")
        send_message('sendMessage', {
            'chat_id': f'your message {text}'
        })
        return HttpResponse("ok", status=200)
    
def send_message(method, data):
    url = TELEGRAM_API_URL + method
    response = requests.post(url, json=data)
    return response.json()



@api_view(['POST'])
def handle_telegram_update(request):
    data = request.data
    chat_id = data['message']['chat']['id']
    username = data['message']['chat'].get('username', '')
    text = data['message']['text']
    print(f"chat id:{chat_id}\nusername: {username}\ntext:{text}")
    # Save user and message 
    user, _ = TelegramUser.objects.get_or_create(chat_id=chat_id, defaults={'username': username})
    Message.objects.create(user=user, text = text)

    return Response({'status':'ok'})




