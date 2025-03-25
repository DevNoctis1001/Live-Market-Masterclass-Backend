from django.shortcuts import render

import json
import base64

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
# from .models import 
from .gmail_service import fetch_email, parse_alert_email

@csrf_exempt
@require_POST
def gmail_webhook(request):
    try:
        if request.method == 'POST':
            message = json.loads(request.body.decode('utf-8'))  
            print(message)
            return JsonResponse({'status': 'success'}, status = 200)
        return JsonResponse({'status': 'Invalid request method'}, status = 400)
        # Verify Pub/Sub message
        # envelope = json.loads(request.body.decode('utf-8'))
        # message = base64.b64decode(envelope['message']['data']).decode('utf-8')
        # email_id = json.loads(message)['emailId']

        # # Fetch and pro23cess email
        # email_msg = fetch_email(email_id)
        # subject, body = parse_alert_email(email_msg)

        # print(f'Subject: {subject}  Body: {body}')
        # Save alert to database

        return HttpResponse(status = 200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status = 400)


# Create your views here.
