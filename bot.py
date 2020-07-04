import logging
import json
import validators
import uuid
import os

from telegram import ParseMode
from telegram.ext import MessageHandler, Filters, Updater
from selenium import webdriver

# Basic logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# requirement I: Receive token from config file
def get_token():
    with open("config.json", "r") as config:
        config = json.loads(config.read())
        token = str(config['token'])
        return token


# Checking if user input is a valid string or a HTTP request
def is_url(string):
    try:
        if validators.url(string):
            return string
        else:
            string = "https:/" + string

            if validators.url(string):
                return string
            else:
                return False

    except ValueError:
        return False


def take_screenshot(link):
    driver = webdriver.Firefox()
    driver.set_window_size(1920, 1080)
    driver.get(link)
    filename = str(uuid.uuid4()) + ".png"
    driver.save_screenshot(f"./pics/{filename}")
    driver.close()
    return filename


# text_handler
def receive_link(update, context):
    global my_screenshot
    user_input = update.message.text
    my_link = is_url(user_input)
    if not my_link:
        reply = "Друг, это не ссылка, я не смогу сделать скриншот"
        pic = ''
    else:
        reply = "Это ссылка, чичас пойду делать скриншот"
        my_screenshot = take_screenshot(my_link)
        pic = open(f"pics/{my_screenshot}", 'rb')

    context.bot.send_message(chat_id=update.effective_chat.id, text=reply, parse_mode=ParseMode.HTML)
    if pic:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=pic, caption="Твой скриншот дебильный...")
        if os.path.exists(f"pics/{my_screenshot}"):
            os.remove(f"pics/{my_screenshot}")


def main():
    updater = Updater(token=get_token(), use_context=True)
    dispatcher = updater.dispatcher

    link_handler = MessageHandler(Filters.text & (~Filters.command), receive_link)
    dispatcher.add_handler(link_handler)

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
