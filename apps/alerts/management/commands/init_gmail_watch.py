from django.core.management.base import BaseCommand
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from django.conf import settings

class Command(BaseCommand):
    help = 'Initialize Gmail watch for push notifications'

    def handle(self, *args, **options) :
        creds = Credentials.from_authorized_user_file(
            settings.GMAIL_CREDENTIALS_PATH,
            settings.GMAIL_SCOPES
        )

        service  = build('gmail', 'v1', credentials=creds)

        response = service.users().watch(
            userId = 'me',
            body = {
                'labelIds' : ['INBOX'],
                'topicName' : 'projects/livemarketmarsterclass/topics/thinkorswim-notifications'
            }
        ).execute()

        self.stdout.write(f'Watch started. History ID: {response['historyId']}')
        