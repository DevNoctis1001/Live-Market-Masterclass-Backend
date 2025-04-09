
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os.path
import re
import asyncio
import threading
import requests
import time

from ..orderdetails import OrderDetail
SCOPES = ["https://mail.google.com/"]

lasttime_filepath = "apps/alerts/utils/EmailFetch/lasttime.txt"

class EmailFetchClass :

  def ParseStringByRe(self, message) :
      
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
          # extractedOrder.print()
      else :
        print("Don't match\n-------------------------------\n")
        return None
        
      return extractedOrder

  def Fetch(self):
    try:
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
    except Exception as e:
      # print(f"Error: {e}")
      return None
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
        return None
      
      with open(lasttime_filepath, 'r') as file:
        last_time = int(file.read())

      max_time=-1
      FetchOrder = None
      for message in messages:
        # print(f"NowTime: {time.strftime('%H:%M:%S', time.localtime())}.{int((time.time() % 1) * 1000):03d}")
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        
        headers = msg['payload']['headers']
        subject = next((header['value'] for header in headers if header['name'] == 'Subject'), None)
        max_time = max(max_time,int(msg['internalDate'])) 
        if int(msg['internalDate']) > last_time :
          print(f"Time : {msg['internalDate']}")
          print("----------------------------------------\n")
          if(FetchOrder == None):
            TempOrder = self.ParseStringByRe(msg['snippet'])
            if TempOrder != None:
              FetchOrder = TempOrder
            print("----------------------------------------\n")
          else :
            TempOrder = self.ParseStringByRe(msg['snippet'])
            if TempOrder != None:
              FetchOrder.Quantity =str( int(FetchOrder.Quantity) + int(TempOrder.Quantity))
        else :
          break
      last_time = max_time
      # FetchOrder.print() 
      threading.Thread(target=self.updateLastTime, args=(last_time,)).start()
      # print(f"Last Time : {last_time}")
      if FetchOrder == None:
        # print("No new messages.")
        return None
      FetchOrder.print()
      # print(f"FetchOrder: {FetchOrder.Quantity}")
      return FetchOrder

    except HttpError as error: 
      print(f"An error occurred: {error}")
  def updateLastTime(self, lastTime):
    with open(lasttime_filepath, 'w') as file:
      file.write(str(lastTime))