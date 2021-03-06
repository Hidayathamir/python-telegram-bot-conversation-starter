import logging
from random import randint
from urllib.request import urlopen
from json import loads
from os import environ

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Get all conversation starter
logger.info('get all conversation starter')
url = "https://raw.githubusercontent.com/Hidayathamir/conversation-starters/main/data.json"
response = urlopen(url)
data_json = loads(response.read())
len_data = len(data_json)


def getConvStarter():
    return data_json[randint(0, len_data)]


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    logger.info('someone run /start')
    msg = getConvStarter()
    opening = 'Use this topic for your conversation.'
    update.message.reply_text(opening)
    update.message.reply_text(msg)


def about(update: Update, context: CallbackContext) -> None:
    msg = "This project is created by [HidayatHamir](https://github.com/Hidayathamir)\n" + "My Social Media in [Here](https://github.com/Hidayathamir#%EF%B8%8F-lets-connect)\n" + \
        "You can see this project in [Here](https://github.com/Hidayathamir/python-telegram-bot-conversation-starter)"
    update.message.reply_markdown_v2(msg)


def main() -> None:
    """Start the bot."""
    logger.info('run main')

    # Hide this
    TOKEN = environ.get('TOKEN')
    PORT = environ.get('PORT', 8443)

    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("about", about))

    # Start the Bot
    updater.start_webhook(
        listen='0.0.0.0',
        port=PORT,
        url_path=TOKEN,
        webhook_url=f'https://conv-starter.herokuapp.com/{TOKEN}'
    )

    updater.idle()


if __name__ == '__main__':
    main()
