import logging
import json
import validators
from urllib.parse import urlparse
from telegram import ParseMode
from telegram.ext import MessageHandler, Filters, Updater
from Screenshot import Screenshot_Clipping
from selenium import webdriver

# Basic logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# requirement I: Receive token from config file
def get_token():
    with open("config.json", "r") as config:
        config = config.read()
        config = json.loads(config)
        token = str(config['token'])
        return token


# Checking if user input is a valid string or a HTTP request
def is_url(string):
    try:
        if validators.domain(string) or validators.url(string):
            return True
        else:
            return False
    except ValueError:
        return False


# text_handler
def make_screenshot(update, context):
    user_input = update.message.text
    if not is_url(user_input):
        reply = "Друг, это не ссылка, я не смогу сделать скриншот"
    else:
        reply = "Это ссылка, чичас пойду делать скриншот"
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply, parse_mode=ParseMode.HTML)


def main():
    updater = Updater(token=get_token(), use_context=True)
    dispatcher = updater.dispatcher

    link_handler = MessageHandler(Filters.text & (~Filters.command), make_screenshot)
    dispatcher.add_handler(link_handler)

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
