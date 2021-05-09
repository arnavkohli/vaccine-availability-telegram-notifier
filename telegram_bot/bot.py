import logging, requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os, re

PORT = int(os.environ.get('PORT', 8443))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = os.getenv('TELEGRAM_BOT_KEY')
REGISTRATION_API = os.getenv('REGISTRATION_API')
CURRENT_DOMAIN = os.getenv('CURRENT_DOMAIN')

def is_valid_indian_pincode(pincode):
    regex = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$"
    pattern = re.compile(regex)
    matches = re.match(pattern, pincode)
    return False if matches == None else True

def insert_update_request(first_name, last_name, telegram_id, telegram_username, chat_id, pincodes):
    url = REGISTRATION_API + "addPincode"
    data = {
        "first_name" : first_name,
        "last_name" : last_name,
        "telegram_id" : telegram_id,
        "telegram_username" : telegram_username,
        "pincodes" : pincodes,
        "chat_id" : chat_id
    }
    response = requests.post(url, json=data)
    print ("response from api", response.json())
    return response.json()

def delete_request(telegram_id, pincodes):
    url = REGISTRATION_API + "removePincode"
    data = {
        "telegram_id" : telegram_id,
        "pincodes" : pincodes
    }
    response = requests.post(url, json=data)
    return response.json()

def list_request(telegram_id):
    url = REGISTRATION_API + "findUser"
    data = {
        "telegram_id" : telegram_id
    }
    response = requests.post(url, json=data)
    return response.json()


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def addPincode(update, context):
    """Send a message when the command /add is issued."""
   
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    telegram_user_id = update.message.from_user.id
    telegram_username = update.message.from_user.username

    print (f"[BOT] /addPincode Request from (username: {telegram_username}; first_name: {first_name}; last_name: {last_name}; telegram_id: {telegram_user_id}) ")
    text = update.message.text
    print ("text", text)
    pincodes = text.split(" ")[1:]
    print ("pincodes", pincodes)

    # Check pincode validity
    if not is_valid_indian_pincode(pincodes[0]):
        update.message.reply_text(f"Invalid Pincode: {pincodes[0]}")
    else:
        chat_id = update.message.chat.id
        print ("chat_id", chat_id)

        data = insert_update_request(first_name, last_name, telegram_user_id, telegram_username, chat_id, pincodes)
        print ("data", data)
        if data:
            user_data = eval(data.get('user_data').replace("null", "None").replace("true", "True").replace("false", "False"))
            print ("user_data", user_data)
            pincodes = user_data.get('pincodes')
            print ("pincodes", pincodes)
            if not pincodes or pincodes == "null":
                update.message.reply_text(f"You have not added any pincodes!")
            else:
                update.message.reply_text(f"Actively Tracking Pincodes: {', '.join(pincodes)}")
        else:
            update.message.reply_text(f"There was an error!")

def removePincode(update, context):
    """Send a message when the command /remove is issued."""
   
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    telegram_user_id = update.message.from_user.id
    telegram_username = update.message.from_user.username

    print (f"[BOT] /removePincode Request from (username: {telegram_username}; first_name: {first_name}; last_name: {last_name}; telegram_id: {telegram_user_id}) ")
    text = update.message.text
    pincodes = text.split(" ")[1:]
    print ("pincodes", pincodes)
    # Check pincode validity
    if not is_valid_indian_pincode(pincodes[0]):
        update.message.reply_text(f"Invalid Pincode: {pincodes[0]}")
    else:
        chat_id = update.message.chat.id

        data = delete_request(telegram_user_id, pincodes)
        print ("data", data)
        if data:
            user_data = eval(data.get('user_data').replace("null", "None").replace("true", "True").replace("false", "False"))
            print ("user_data", user_data)
            pincodes = user_data.get('pincodes')
            print ("pincodes", pincodes)
            if not pincodes or pincodes == 'null':
                update.message.reply_text(f"You have not added any pincodes!")
            else:
                update.message.reply_text(f"Actively Tracking Pincodes: {', '.join(pincodes)}")
        else:
            update.message.reply_text(f"There was an error!")

def listPincodes(update, context):
    """Send a message when the command /list is issued."""
   
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    telegram_user_id = update.message.from_user.id
    telegram_username = update.message.from_user.username

    print (f"[BOT] /listPincodes Request from (username: {telegram_username}; first_name: {first_name}; last_name: {last_name}; telegram_id: {telegram_user_id}) ")
    text = update.message.text
    pincodes = text.split(" ")[1:]
    chat_id = update.message.chat.id

    data = list_request(telegram_user_id)
    print ("data", data)
    if data and data != 'null':
        user_data = eval(data.get("user").replace("null", "None").replace("true", "True").replace("false", "False"))
        print ("user_data", user_data)
        pincodes = user_data.get('pincodes')
        print ("pincodes", pincodes)
        if not pincodes or pincodes == 'null':
            update.message.reply_text(f"You have not added any pincodes!")
        else:
            update.message.reply_text(f"Actively Tracking Pincodes: {', '.join(pincodes)}")
    else:
        update.message.reply_text(f"You have not added any pincodes!")

def help(update, context):
    """Send a message when the command /help is issued."""
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    telegram_user_id = update.message.from_user.id
    telegram_username = update.message.from_user.username

    print (f"[BOT] /help Request from (username: {telegram_username}; first_name: {first_name}; last_name: {last_name}; telegram_id: {telegram_user_id}) ")
    message = '''Hey! Im the COVID19VANBot (India).\nWe are in beta. Scheduler is scheduled to run at 7AM IST and 5PM IST.\n\nCommands:\n/add PINCODE - Add a pincode to track.\n\n/remove PINCODE - Stop tracking a pincode.\n\n/list - List all actively tracking pincodes.'''
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
    #updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()