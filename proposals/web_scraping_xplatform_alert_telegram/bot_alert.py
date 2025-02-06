import telegram
import asyncio

class BotAlert(object):

    fake = False
    def __init__(self, bot_token=None):
        self.bot_token = bot_token
        if not bot_token:
            fake = True

    def send_message(self, chat_id, msg):
        if self.bot_token:
            bot = telegram.Bot(token=self.bot_token)
            asyncio.run(bot.send_message(chat_id=chat_id, text=msg))
        else:
            print("Token was not set. Message to be sent was: \n %s", msg)

    @staticmethod
    def print_info():
        print('Step1: Create bot via chat with @BotFather and typing /newbot')
        print('Step2: Follow the instructions to choose a name and username for your bot.')
        print('       After completing these steps, the BotFather will provide you with an API token (keep it safe).')
        print('Step3: Create chat and add your new bot, then to get chat_id run ')
        print('       https://api.telegram.org/bot<YourBOTToken>/getUpdates')

if __name__ == "__main__":
    # Your bot token
    BOT_TOKEN = None
    # Your chat ID
    # To get chat id run https://api.telegram.org/bot<YourBOTToken>/getUpdates
    CHAT_ID = '-4706647839'
    # Message to send
    MESSAGE = 'Hey there!'

    # test_bot = BotAlert(BOT_TOKEN)
    # test_bot.send_message(CHAT_ID, MESSAGE)
    BotAlert().print_info()