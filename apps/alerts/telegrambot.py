from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from threading import Thread
import time
import asyncio

class TelegramBot:
    def __init__(self,token):
        self.token = token
        self.application = None
        self.user_name  = None
        self.user_id = None
        self.chat_id = None

    # Function to handle the /start command
    async def start(self, update: Update, context: CallbackContext) -> None:
        user = update.effective_user
        self.user_name = user.username if user.username else "User"
        self.user_id = user.id
        self.chat_id= update.message.chat_id

        print(f"Username : {self.user_name}, User ID : {self.user_id} Chat ID: {self.chat_id}")
        
        await update.message.reply_text(f'Hello {self.user_name}! You are now subscribed to event notifications.')
 
    # Function to handle user messages
    async def handle_message(self, update: Update, context: CallbackContext) -> None : 
        user = update.effective_user
        self.user_name = user.username if user.username else "User"
        self.user_id = user.id
        user_message = update.message.text.lower()      
        self.chat_id = update.message.chat_id
        print(f"Username : {self.user_name}, User ID : {self.user_id} Chat ID: {self.chat_id}")

        if user_message == 'stop' : 
            await update.message.reply_text('You have stopped the subscription.')
        else :
            await update.message.reply_text(f'You said: {user_message}')
    
    def run_async(self, coroutine):
        """Helper method to run async code from sync context"""
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(coroutine)

    async def send_notification(self, message:str): 
        try:
            await self.application.bot.send_message(chat_id=self.chat_id, text= message)
        except Exception as e:
            print(f"An error occurred while sending the notification to {self.chat_id}: {e}")

    def send_event_notification(self): 
        time.sleep(10)

        if self.chat_id:
            self.run_async(self.send_notification("Hello"))
        else:
            print("No chat_id available yet. Message not sent.")


    def main(self):
        self.application  = Application.builder().token(self.token).build()
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        # self.send_event_notification() 
        print(f"This is Main")
        Thread(target=self.send_event_notification, daemon=True).start()
        self.application.run_polling()

if __name__ == "__main__":
    telegram_bot = TelegramBot("7598620067:AAFMSpKJaxZ4gyXCyLW78vi5n5ivuC1b_zM")
    telegram_bot.main()