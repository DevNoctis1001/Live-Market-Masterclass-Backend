import os.path
import re
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# If modifying these scopes, delete the file token.json.

# SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
SCOPES = ["https://mail.google.com/"]

# https://console.cloud.google.com/apis/credentials

# with open('profile.json', 'r') as file:
#   profile = json.load(file)
def main():
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

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    sender_email = "danemanji0089@gmail.com"
    recipient_email = 'marketmasterclasstosalerts@gmail.com'
    # start_date = (datetime.now(pytz.utc) - timedelta(seconds=600))
    # print(start_date)
    # end_date = datetime.now().strftime('%Y/%m/%d')
    # query = f"from:{sender_email} to:{recipient_email} after:{start_date} before:{end_date}"
    query = f"from:{sender_email} to:{recipient_email}"
    results = service.users().messages().list(userId="me", q=query).execute()
    messages = results.get("messages", [])
    if not messages:
      print("No messages found.")
      return
    # print("Messages sent to the recipient:")
    first_message_id = messages[0]['id']
    msg = service.users().messages().get(userId='me', id=first_message_id).execute()
    # print("Message deleted successfully.")
    # snippet = msg['snippet']
    # print(f"subject:  snippet: {snippet} ")
    # print(f"Snipet: {snippet}")
    # otp_match = re.search(r'\b\d{6}\b', snippet)
    # if otp_match:
    #   otp = otp_match.group(0)
    #   print(f"Extracted OTP: {otp}")
    #   service.users().messages().delete(userId='me', id=first_message_id).execute()
    #   print("Message deleted successfully.")
    # else:
    #   print("OTP not found in the snippet.")

    for message in messages:
      msg = service.users().messages().get(userId='me', id=message['id']).execute()
      headers = msg['payload']['headers']
      subject = next((header['value'] for header in headers if header['name'] == 'Subject'), None)
      print(f"Message ID: {message['id']}, Subject: {subject}, Snippet: {msg['snippet']}")
    
    service.users().messages().delete(userId='me', id=first_message_id).execute()

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  while True:
    main()