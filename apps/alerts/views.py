from django.shortcuts import render

import json
import os
import base64

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# from .models import 
from .gmail_service import fetch_email, parse_alert_email
import apps.orderdetails as orderdetails
# from orderdetails import OrderDetail


SCOPES = ["https://mail.google.com/"]
@csrf_exempt
# @require_POST
def gmail_webhook(request):
    """
    Django webhook endpoint for Gmail Pub/Sub notifications
    """
    print("this is webhook")
    try:
        envelope = json.loads(request.body)

        # Verify this is a Pub/Sub message
        if not envelope.get('message'):
            return HttpResponse('Bad Request: Not a Pub/Sub message', status=400)
        
        pubsub_message = envelope['message']
        message_data = base64.b64decode(pubsub_message['data']).decode('utf-8')

        # Parse the Gmail message details
        gmail_notification = json.loads(message_data)

        # Extract message ID from notification
        message_id  = gmail_notification.get('messageId')

        # Here you would use Google Gmail API to fetch full message details

        order_details = parse_gmail_message(message_id)
        
        # Process the order details
        # ...

        return HttpResponse('OK', status = 200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status = 400)
    
def get_credentials():
    
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )                                                                                                                                                                 
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds
        

def parse_gmail_message(message_id) :
    """
    Fetch and parse full Gmail message using Google Gmail API
    """

    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    sender_email = "alerts@thinkorswim.com"
    recipient_email = 'marketmasterclasstosalerts@gmail.com' 
    query = f"from:{sender_email} to:{recipient_email}"
    results = service.users().messages().list(userId="me", q=query).execute()
    messages = results.get("messages", [])

    if not messages:
        print("No messages found.")
        return 
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        headers = msg['payload']['headers']
        subject = next((header['value'] for header in headers if header['name'] == 'Subject'), None)
    #   ParseStringByRe(msg['snippet'])
        order_details = orderdetails.OrderDetail()
        order_details = parse_alert_email(msg['snippet'])
        order_details.print()
      


# Create your views here.
