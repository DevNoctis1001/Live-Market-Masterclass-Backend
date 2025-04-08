from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from threading import Thread
import time
import asyncio
import logging
from  .EmailFetch.email_fetch import EmailFetchClass

import json

users_filepath ='apps/alerts/utils/activeusers.json'

class TelegramBot:

    _instance = None

    @classmethod
    def get_instance(cls, token=None):
        if cls._instance is None and token:
            cls._instance = cls(token)
        return cls._instance

    def __init__(self,token):
        if TelegramBot._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() instead")
        
        self.token = token
        self.application = None
        self.chat_ids=set()  # Store chat IDs that have interacted with the bot
        self.user_name  = None
        self.user_id = None
        self.chat_id = None
        self._bot_thread = None
        self._is_running = False
        self._emailfetch_thread= None
        self._email_trigger_class = None

    # Function to handle the /start command
    async def start(self, update: Update, context: CallbackContext) -> None:
        user = update.effective_user
        self.user_name = user.username if user.username else "User"
        self.user_id = user.id
        self.chat_id= update.message.chat_id

        self.append_user_onusers()
        print(f"Username : {self.user_name}, User ID : {self.user_id} Chat ID: {self.chat_id}")
        if update.effective_chat:
            self.chat_ids.add(update.effective_chat.id)
            await update.message.reply_text(f'Hello {self.user_name}! You are now subscribed to event notifications.')
    
    # Update activeusers.json (stop)
    def update_subscribe_onusers(self):
        with open(users_filepath, 'r') as file:
            users = json.load(file)
        for active_user in users:
            if active_user['userid'] == self.user_id:
                active_user['subscribed'] = 0
        with open(users_filepath, 'w') as file:
            json.dump(users, file, indent=4)

    # Update activeusers.json (start)
    def append_user_onusers(self):
        
        with open(users_filepath, 'r') as file:
            users = json.load(file)
        for active_user in users:
            if active_user['userid'] == self.user_id:
                return
        users.append({"username":self.user_name,"userid": self.user_id, "subscribed": 1})
        print(f"User {self.user_name} with ID {self.user_id} is now subscribed.")
        with open(users_filepath, 'w') as file:
            json.dump(users, file, indent=4)


    # Function to handle user messages
    async def handle_message(self, update: Update, context: CallbackContext) -> None : 
        user = update.effective_user
        self.user_name = user.username if user.username else "User"
        self.user_id = user.id
        user_message = update.message.text.lower()      
        self.chat_id = update.message.chat_id
        # print(f"Username : {self.user_name}, User ID : {self.user_id} Chat ID: {self.chat_id}")
        if update.effective_chat:
            self.chat_ids.add(update.effective_chat.id)
            if user_message == 'start':
                self.append_user_onusers()
                await update.message.reply_text(f'Hello {self.user_name}! You are now subscribed to event notifications.')
            elif user_message == 'stop':
                self.update_subscribe_onusers()
                await update.message.reply_text('You have stopped the subscription.')
            else:
                await update.message.reply_text(f'You said: {user_message}')
    
    def run_async(self, coroutine):
        """Helper method to run async code from sync context"""
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(coroutine)
    
    # Direct send the notification to active users
    async def send_notification_direct(self,user_id:str, message:str): 
        try:
            await self.application.bot.send_message(chat_id=user_id, text= message)
            return True
        except Exception as e:
            print(f"An error occurred while sending the notification: {e}")
            return False
        
    
    async def send_notification(self, message:str): 
        try:
            await self.application.bot.send_message(chat_id=self.chat_id, text= message)
            return True
        except Exception as e:
            print(f"An error occurred while sending the notification to {self.chat_id}: {e}")
            return False

    def notify(self,user_id:str, message: str):
        """
        Public method to send notifications from Django views.
        """ 
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Run the async function
        return loop.run_until_complete(self.send_notification_direct(user_id, message))
    
    def _bot_thread_function(self):
        """
        Function to run the bot in a separate thread.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self._is_running = True

        # Setup the application
        self.application = Application.builder().token(self.token).build()
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

        # Run the bot
        print("Telegram bot is running...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    def email_trigger(self):
        #  ParseStringByRe
        while True:
            result = self._email_trigger_class.Fetch()
            # print(f'Email Trigger Result {result}')
            if result is None:
                continue
            else:
                
                with open(users_filepath, "r") as file:
                    users = json.load(file)

                if result.Action == "SOLD":   
                    message = "Live Market Masterclass\n" \
                    "Exit Alert (Educational Purposes Only)\n" \
                    "🚨 Educational Exit Example 🚨\n" \
                    "Based on our course, here is an example of an exit trade today:\n\n" \
                    f"{result.Expiry} {result.Symbol} ${result.Strike} strike {result.ContractType} @ ${result.ContractPrice} per contract (+20 contracts).\n\n" \
                    "Exit Reason: Following risk management principles.\n" \
                    "📌 Disclaimer: This is an educational example only and should not be interpreted as investment advice, a solicitation, or a recommendation to take any trading action. This content does not constitute financial advice, and all market participants should make independent trading decisions based on their own analysis and risk tolerance. We do not guarantee any profits or outcomes from applying course concepts. Please consult a qualified financial professional before making any investment decisions.\n\n" \
                    "Reply STOP to unsubscribe.\n"
                else :
                    message = "Live Market Masterclass\n" \
                    "Entry Alert (Educational Purposes Only)\n" \
                    "🚨 Educational Trade Example 🚨\n" \
                    "Based on our course, here is an example of an entry trade today:\n\n" \
                    f"{result.Action} {result.Expiry} {result.Symbol} ${result.Strike} strike {result.ContractType} @ ${result.ContractPrice} per contract (+20 contracts).\n\n" \
                    "Target Profit: +20%\n" \
                    "Stop Loss: -15% (tight risk management)\n" \
                    "📌 Disclaimer: This example is for educational purposes only and is not a recommendation to buy, sell, or hold any security. This is not financial, investment, or trading advice and should not be relied upon for making financial decisions. All trading involves risk, and past performance is not indicative of future results. Always conduct your own research and consult with a licensed financial professional before making any investment decisions.\n\n" \
                    "Reply STOP to unsubscribe."

                print(users)
                for user in users:
                    if user['subscribed'] == 0: continue
                    if result.Action == "SOLD" and  user['subscribed'] != 2: continue
                    print(f'userID: {user['userid']} scubscribed: {user['subscribed']}')
                    Thread(target=self.notify, args=(user['userid'], message)).start()
                    # self.notify(user['userid'], message=message)

    def start_bot(self):
        """
        Start the bot in a separate thread.
        """
        if self._bot_thread is None or not self._bot_thread.is_alive():
            self._bot_thread = Thread(target=self._bot_thread_function, daemon=True)
            self._bot_thread.start()
            print("Telegram bot thread started.")
            if self._emailfetch_thread is None or not self._emailfetch_thread.is_alive():
                if self._email_trigger_class is None:
                    self._email_trigger_class = EmailFetchClass()
                self._emailfetch_thread = Thread(target = self.email_trigger, daemon=True)
                self._emailfetch_thread.start()
                print("Email Fetch Thread started.")
            return True
        return False
    
    def main(self):

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  level=logging.INFO)

        """
        For standalone usage
        """
        self.start_bot()

        # # Keep the main thread alive
        # try:
        #     while True:
        #         time.sleep(10)
        #         
        # except KeyboardInterrupt:
        #     print("Bot stopped.") 

if __name__ == "__main__":
    telegram_bot = TelegramBot("7598620067:AAFMSpKJaxZ4gyXCyLW78vi5n5ivuC1b_zM")
    telegram_bot.main()