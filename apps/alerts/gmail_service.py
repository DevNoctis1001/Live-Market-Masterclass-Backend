import os
import base64
import email
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from django.conf import settings

def get_gmail_service():
    creds = Credentials.from_authorized_user_file(
        settings.GMAIL_CREDENTIALS_PATH, 
        settings.GMAIL_SCOPES 
    )

    return build('gmail', 'v1', credentials= creds)

def fetch_email(message_id):
    service = get_gmail_service()
    msg = service.users().message().get(
        userId = 'me',
        id = message_id,
        format = 'raw'
    ).execute()

    raw_email  = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
    return email.message_from_bytes(raw_email)

def parse_alert_email(email_msg):
    subject = email_msg['subject']
    body =""

    if email_msg.is_multipart():
        for part in email_msg.walk():
            if part.get_content_type() == 'text/plan':
                body = part.get_payload()
    else :
        body = email_msg.get_payload()
    
    return subject, body

