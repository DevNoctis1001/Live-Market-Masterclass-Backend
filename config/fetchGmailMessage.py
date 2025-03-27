import os.path
import re
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# If modifying these scopes, delete the file token.json.

# Order class
class OrderDetail:
    def __init__(self):
        self.OrderId = ""
        self.Action = ""
        self.Quantity = ""
        self.Symbol = ""
        self.Shares = ""
        self.OptionType = ""
        self.Expiry = ""
        self.Strike = ""
        self.ContractType = ""
        self.ContractPrice = ""
        self.LastPrice = ""
        self.BidPrice = ""
        self.AskPrice = ""
        self.MarkPrice = ""
        self.ClosePrice = ""
        self.Account = ""

    def print(self):        
        print(f"OrderId: {self.OrderId}")
        print(f"Action: {self.Action}")
        print(f"Quantity: {self.Quantity}")
        print(f"Symbol: {self.Symbol}")
        print(f"Shares: {self.Shares}")
        print(f"OptionType: {self.OptionType}")
        print(f"Expiry: {self.Expiry}")
        print(f"Strike: {self.Strike}")
        print(f"ContractType: {self.ContractType}")
        print(f"ContractPrice: {self.ContractPrice}")
        print(f"LastPrice: {self.LastPrice}")
        print(f"BidPrice: {self.BidPrice}")
        print(f"AskPrice: {self.AskPrice}")
        print(f"MarkPrice: {self.MarkPrice}")
        print(f"ClosePrice: {self.ClosePrice}")
        print(f"Account: {self.Account}")
        print("----------------------------------------\n")

SCOPES = ["https://mail.google.com/"]



def ParseStringByRe(message) :
    
    print(f"Messge: \n {message}\n")
    pattern  = r'(#\d+) ([A-Z]+) ([+-]?\d+) ([A-Z]+) (\d+) \((\w+)\) (\d+) (\w+) (\d+) (\d+) (\w+) @(\d*\.\d+)LAST=(\d+\.\d+) BID=(\d+\.\d+) ASK=(\d+\.\d+) MARK=(\d+\.\d+) CLOSE=(\w+) , ACCOUNT (\*{5}\w+)'
    match = re.match(pattern, message)
    extractedOrder = OrderDetail()

    if match != None:
        extractedOrder.OrderId     =   match.group(1)
        extractedOrder.Action      =   match.group(2)
        extractedOrder.Quantity    =   match.group(3)
        extractedOrder.Symbol      =   match.group(4)
        extractedOrder.Shares      =   match.group(5)
        extractedOrder.OptionType  =   match.group(6)
        extractedOrder.Expiry      =   match.group(7) + " " + match.group(8) + " " + match.group(9)
        extractedOrder.Strike      =   match.group(10)
        extractedOrder.ContractType=   match.group(11)
        extractedOrder.ContractPrice=  match.group(12)
        extractedOrder.LastPrice   =   match.group(13)
        extractedOrder.BidPrice    =   match.group(14)
        extractedOrder.AskPrice    =   match.group(15)
        extractedOrder.MarkPrice   =   match.group(16)
        extractedOrder.ClosePrice  =   match.group(17)
        extractedOrder.Account     =   match.group(18)
        extractedOrder.print()
    else :
       print("Don't match")
  

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
      ParseStringByRe(msg['snippet'])
      
      # print(f"Message ID: {message['id']}, Subject: {subject}, Snippet: {msg['snippet']}") 

  except HttpError as error: 
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  while True:
    main()