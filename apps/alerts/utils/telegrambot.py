from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from threading import Thread
import time
import asyncio
import logging
from  .EmailFetch.email_fetch import EmailFetchClass
from datetime import date, datetime
import pytz
import json

est = pytz.timezone('US/Eastern')
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
        try:
            print("start command detected")
            user = update.effective_user
            self.user_name = user.username if user.username else "User"
            self.user_id = user.id
            self.chat_id= update.message.chat_id

            self.append_user_onusers()
            self.modify_user_onusers(0)
            print(f"Username : {self.user_name}, User ID : {self.user_id} Chat ID: {self.chat_id}")
            print("start command completed")
            if update.effective_chat:
                self.chat_ids.add(update.effective_chat.id)
                # await update.message.reply_text(f'Hello {self.user_name}! You are now subscribed to event notifications.')


            keyboard = [
                [InlineKeyboardButton("📖 Read Full Disclaimer", callback_data="read_disclaimer")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
                
            await update.message.reply_text(
                f'📜    Welcome to LiveMarketMasterClassBot! \n \n'
                'Before we begin, please read and accept our Educational Trade Alerts Disclaimer to proceed. \n \n'
                'All trade examples are for educational purposes only and must not be used as financial advice. \n \n'
                'We are not liable for any financial losses resulting from actions taken based on this content. \n \n'
                'Tap "Read Full Disclaimer" below to continue.',
                reply_markup=reply_markup
            )
        except Exception as e:
            # print(f"Error in start command: {e}")
            pass


    # Function to handle the /stop command
    
    async def stop(self, update:Update, context: CallbackContext) -> None:
        user = update.effective_user
        self.user_name = user.username if user.username else "User"
        self.user_id = user.id
        self.chat_id= update.message.chat_id

        await update.message.reply_text(
            '🛑 You have stopped the subscription.'
        )

        self.modify_user_onusers(0)


    async def upgrade(self, update:Update, context: CallbackContext) -> None:
        user = update.effective_user
        self.user_name = user.username if user.username else "User"
        self.user_id = user.id
        self.chat_id= update.message.chat_id

        await update.message.reply_text(
            '👋 Welcome to Platinum Notifications! \n \n'
            'As a Platinum member, you will receive both Entry and Exit Alerts to support your learning and strategy development. \n \n'
            '📌 Reminder: These alerts are for educational use only. They are not financial advice or recommendations to buy, sell, or trade any security. Our goal is to help you study real-time examples that align with what you’ve learned in the course, so you can strengthen your understanding and confidence. \n \n'
            'We are not liable for any trading decisions or financial outcomes. Always do your own research and speak to a qualified professional before making any investment choices. \n \n'
        )

        self.modify_user_onusers(2)

    async def help(self, update:Update, context: CallbackContext) -> None:
        await update.message.reply_text(
            '👋  Coming soon! \n \n'
        )

    async def btn_handler(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        await query.answer()  # Acknowledge the button click

        keyboard = [
            [
                InlineKeyboardButton("✅ YES, I AGREE AND UNDERSTAND", callback_data="accept_terms"),
            ],
            [
                InlineKeyboardButton("❌ NO, I DO NOT AGREE", callback_data="decline_terms")
            ]
                
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if query.data == "read_disclaimer":
            await self.reply_disclaimer(query, reply_markup)
        if query.data == "accept_terms":
            await self.reply_accept_term(query)
        if query.data == "decline_terms":
            await self.reply_decline_term(query)


    async def reply_accept_term(self, query):
        await query.message.reply_text(
                        text=(
                            "✅ Confirmation: \n\n"
                            f"@{self.user_name}, you have agreed to the Terms & Conditions on {datetime.now(est).strftime("%Y-%m-%d %H:%M:%S")} EST. \n\n"
                            "Thank you for your acknowledgment. This record may be used for verification and compliance purposes. You may now continue."
                        ),
                        parse_mode='Markdown'
                    )

        await query.message.reply_text(
                text=(
                    "👋 Welcome to Gold Notifications! \n\n"
                    "You will now begin receiving Entry Alerts based on concepts taught in our trading course. \n\n"
                    "📌 Please note: All alerts are provided strictly for educational purposes. They are not investment advice, trade recommendations, or signals to take action in any live market. Our examples are intended to help you understand market structure, risk management, and strategy as outlined in the course. \n\n"
                    "You are solely responsible for your trading decisions. Always consult a licensed financial advisor before making financial decisions."
                
                ),
                parse_mode='Markdown'
            )

        self.modify_user_onusers(1)

    async def reply_decline_term(self, query):
        await query.message.reply_text(
                text=(
                    "❌ You have declined the disclaimer. \n\n"
                    "You will not receive educational trade alerts or course examples. If you change your mind, type /start again to review the disclaimer."
                ),
                parse_mode='Markdown'
            )
        self.modify_user_onusers(0)

    async def reply_disclaimer(self, query, reply_markup):
        await query.message.reply_text(
                text=(
                    "📌 FULL DISCLAIMER & CONSENT AGREEMENT \n\n"
                    "By subscribing to and receiving trade alerts from this bot, you agree that: \n\n"
                    "1️⃣ Alerts are for educational purposes only and are not financial or investment advice. \n\n"
                    "2️⃣ You should not follow these trades in real markets. They're simulations based on course concepts. \n\n"
                    "3️⃣ We are not liable for any financial losses you incur by acting on this content. \n\n"
                    "4️⃣ All trading involves risk, and past performance does not guarantee future results. \n\n"
                    "5️⃣ You accept full responsibility for your own decisions, risk tolerance, and portfolio management. \n\n"
                    "6️⃣ Always consult with a licensed financial advisor before making any investment. \n\n"
                    "By accepting, you confirm that you have read, understood, and agreed to these terms. \n\n"
                    "Do you accept these terms?"
                ),
                reply_markup=reply_markup,
                parse_mode='Markdown'
        )

    # Update activeusers.json (stop)
    def update_subscribe_onusers(self):
        try:
            with open(users_filepath, 'r') as file:
                users = json.load(file)
            for active_user in users:
                if active_user['userid'] == self.user_id:
                    active_user['subscribed'] = 0
            with open(users_filepath, 'w') as file:
                json.dump(users, file, indent=4)
        except Exception as e:
            pass

    # Update activeusers.json (start)
    def append_user_onusers(self):
        try :
            with open(users_filepath, 'r') as file:
                users = json.load(file)
            for active_user in users:
                if active_user['userid'] == self.user_id:
                    return
            users.append({"username":self.user_name,"userid": self.user_id, "subscribed": 0})
            print(f"User {self.user_name} with ID {self.user_id} is now subscribed.")
            with open(users_filepath, 'w') as file:
                json.dump(users, file, indent=4)
        except Exception as e:
            pass

    def modify_user_onusers(self, subscribed):
        try:
            with open(users_filepath, 'r') as file:
                users = json.load(file)

            user_found = False
            for user in users:
                if user['userid'] == self.user_id:
                    # Modify existing user data
                    user['subscribed'] = subscribed  # or any logic you want here
                    print(f"User {self.user_name} with ID {self.user_id} has been updated.")
                    break

            with open(users_filepath, 'w') as file:
                json.dump(users, file, indent=4)
        except Exception as e:
            pass 



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
        try:
            loop = asyncio.new_event_loop()
            return loop.run_until_complete(coroutine)
        except Exception as e:
            return None
    
    # Direct send the notification to active users
    async def send_notification_direct(self,user_id:str, message:str): 
        try:
            await self.application.bot.send_message(chat_id=user_id, text= message)
            return True
        except Exception as e:
            # print(f"An error occurred while sending the notification: {e}")
            return False
        
    
    async def send_notification(self, message:str): 
        try:
            await self.application.bot.send_message(chat_id=self.chat_id, text= message)
            return True
        except Exception as e:
            # print(f"An error occurred while sending the notification to {self.chat_id}: {e}")
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
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self._is_running = True

            print("Thread start")
            # Setup the application
            self.application = Application.builder().token(self.token).build()
            self.application.add_handler(CommandHandler("start", self.start))
            self.application.add_handler(CommandHandler("upgrade", self.upgrade))
            self.application.add_handler(CommandHandler("help", self.help))
            self.application.add_handler(CommandHandler("stop", self.stop))
            self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
            self.application.add_handler(CallbackQueryHandler(self.btn_handler))

            # Run the bot
            print("Telegram bot is running...")
            self.application.run_polling(allowed_updates=Update.ALL_TYPES)
        except Exception as e:
            # print(f"An error occurred in the bot thread: {e}")
            pass


    def email_trigger(self):
        #  ParseStringByRe
        try:
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
                        "Exit Alert (Educational Purposes Only)\n\n" \
                        "⚠️  Educational Exit Example ⚠️ \n" \
                        "Here is the exit update for today’s trade example:\n\n" \
                        "Trade closed:\n"  \
                        f"{result.Expiry} {result.Symbol} ${result.Strike} strike {result.ContractType} \n" \
                        f"Exit Price: ${result.ContractPrice} per contract\n\n" \
                        "This exit follows our predefined plan and demonstrates the importance of disciplined risk management.\n\n" \
                        "📌 Disclaimer: This trade update is for educational purposes only and is not a recommendation to buy, sell, or hold any financial instrument. It does not constitute financial, investment, or trading advice. All forms of trading involve risk, and past performance is not indicative of future results. Always do your own research and consult with a licensed financial professional before making any financial decisions.\n\n" \
                        "You are not required to follow this trade. Please always remember to trade in a paper money account or virtual simulator until you are proven profitable to be trading in the live markets.\n\n" \
                        "To unsubscribe, reply STOP."
                    else :
                        message = "Live Market Masterclass\n" \
                        "Entry Alert (Educational Purposes Only)\n\n" \
                        "⚠️  Educational Trade Example ⚠️ \n" \
                        "The following trade setup is shared strictly as an illustration aligned with the strategies taught in our course:\n\n" \
                        "Trade Example:\n" \
                        f"{result.Action} {result.Expiry} {result.Symbol} ${result.Strike} strike {result.ContractType} @ ${result.ContractPrice} per contract (+20 contracts).\n\n" \
                        "Exit Plan: \n\n" \
                        "Target Profit: +20%\n\n" \
                        "Stop Loss: -15% (tight risk management)\n\n" \
                        "📌 Disclaimer: This content is intended solely for educational and informational purposes. It does not constitute financial, investment, or trading advice and must not be interpreted as a recommendation to take any specific action in the market. We are not registered investment advisors, and this communication is not an offer or solicitation to buy or sell any security. All trading involves substantial risk, and individuals are solely responsible for their own investment decisions. Past performance is not indicative of future results.\n\n" \
                        "You are not required to take this trade. Please always remember to use a paper money account or trading simulator until you have demonstrated consistent profitability in the live markets.\n\n" \
                        "To unsubscribe, reply STOP."

                    print(users)
                    for user in users:
                        if user['subscribed'] == 0: continue
                        if result.Action == "SOLD" and  user['subscribed'] != 2: continue
                        print(f'userID: {user['userid']} scubscribed: {user['subscribed']}')
                        Thread(target=self.notify, args=(user['userid'], message)).start()
                        # self.notify(user['userid'], message=message)
        except Exception as e:
            print(f"Error in email_trigger: {e}")


    def start_bot(self):
        """
        Start the bot in a separate thread.
        """

        try: 
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
        except Exception as e:
            # print(f"Error starting bot: {e}")
            return False
    def main(self):
 
        self.start_bot()


if __name__ == "__main__":
    telegram_bot = TelegramBot("7598620067:AAFMSpKJaxZ4gyXCyLW78vi5n5ivuC1b_zM")
    telegram_bot.main()