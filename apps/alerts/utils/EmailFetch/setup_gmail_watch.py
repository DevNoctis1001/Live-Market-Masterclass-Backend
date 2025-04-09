import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_gmail_service() :
    """ Gets authenticated Gmail API service"""
    creds = None

    # The file token.pickle stores the user's access and refresh tokens.

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (vaild) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else :
            # Path to your downloaded OAuth client secret
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)   

    return build('gmail', 'v1', credentials=creds)

def setup_gmail_watch():
    """ Sets up Gmail API watch on the user's inbox."""
    service = get_gmail_service()

    # Set up the watch request
    request = {
        'labelIds': ['INBOX'],
        'topicName': 'projects/livemarketmarsterclass/topics/thinkorswim-notifications',
        'labelFilterBehavior': 'INCLUDE'
    }

    # Execute the watch request 
    response = service.users().watch(userId='me', body = request).execute()
    print(f"Watch setup successfully. Expires in {response.get('expiration')} ms")
    return response

if __name__ == '__main__':
    setup_gmail_watch()
