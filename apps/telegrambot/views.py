from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TelegramUser, Message

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




