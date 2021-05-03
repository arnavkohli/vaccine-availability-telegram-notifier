import logging, requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

PORT = int(os.environ.get('PORT', 8443))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = os.getenv('TELEGRAM_BOT_KEY')
REGISTRATION_API = os.getenv('REGISTRATION_API')
CURRENT_DOMAIN = os.getenv('CURRENT_DOMAIN')


def insert_update_request(telegram_username, chat_id, pincodes):
    url = REGISTRATION_API + "addPincode"
    data = {
        "telegram_username" : telegram_username,
        "pincodes" : pincodes,
        "chat_id" : chat_id
    }
    response = requests.post(url, json=data)
    return response.json()

def delete_request(telegram_username, pincodes):
    url = REGISTRATION_API + "removePincode"
    data = {
        "telegram_username" : telegram_username,
        "pincodes" : pincodes
    }
    response = requests.post(url, json=data)
    return response.json()

def list_request(telegram_username):
    url = REGISTRATION_API + "findUser"
    data = {
        "telegram_username" : telegram_username
    }
    response = requests.post(url, json=data)
    return response.json()


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def addPincode(update, context):
    """Send a message when the command /start is issued."""
   
    username = update.message.from_user.id
    print (f"[BOT] /addPincode Request from {username}")
    text = update.message.text
    pincodes = text.split(" ")[1:]
    chat_id = update.message.chat.id

    data = insert_update_request(username, chat_id, pincodes)

    user_data = data.get('user_data')

    if data:
        pincodes = eval(user_data).get('pincodes')
        if not pincodes or pincodes == 'null':
            update.message.reply_text(f"You have not added any pincodes!")
        else:
            update.message.reply_text(f"Actively Tracking Pincodes: {', '.join(pincodes)}")
    else:
        update.message.reply_text(f"There was an error!")

def removePincode(update, context):
    """Send a message when the command /start is issued."""
   
    username = update.message.from_user.id
    print (f"[BOT] /removePincode Request from {username}")
    text = update.message.text
    pincodes = text.split(" ")[1:]
    chat_id = update.message.chat.id

    data = delete_request(username, pincodes)

    user_data = data.get('user_data')

    if data:
        pincodes = eval(user_data).get('pincodes')
        if not pincodes or pincodes == 'null':
            update.message.reply_text(f"You have not added any pincodes!")
        else:
            update.message.reply_text(f"Actively Tracking Pincodes: {', '.join(pincodes)}")
    else:
        update.message.reply_text(f"There was an error!")

def listPincodes(update, context):
    """Send a message when the command /start is issued."""
   
    username = update.message.from_user.id
    print (f"[BOT] /listPincodes Request from {username}")
    text = update.message.text
    pincodes = text.split(" ")[1:]
    chat_id = update.message.chat.id

    data = list_request(username)

    user_data = data.get('user')
    if user_data and user_data != 'null':
        pincodes = eval(user_data).get('pincodes')
        if not pincodes or pincodes == 'null':
            update.message.reply_text(f"You have not added any pincodes!")
        else:
            update.message.reply_text(f"Actively Tracking Pincodes: {', '.join(pincodes)}")
    else:
        update.message.reply_text(f"You have not added any pincodes!")

def help(update, context):
    """Send a message when the command /help is issued."""
    username = update.message.from_user.id
    print (f"[BOT] /help Request from {username}")
    message = '''Hey! Im the COVID19VANBot (India). Pipelines are currently down but you can still register and will opted for notifications whenever they are back up!\n
    Commands:\n
    1. /add <PINCODE>\n
    2. /remove <PINCODE>\n
    3. /list
    '''
    update.message.reply_text(message)

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text("Invalid command! Type /help for a list of valid commands.")

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("add", addPincode))
    dp.add_handler(CommandHandler("remove", removePincode))
    dp.add_handler(CommandHandler("list", listPincodes))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url=CURRENT_DOMAIN + TOKEN)

    # Local testing
    # updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()