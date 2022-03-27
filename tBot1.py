import telebot
from flask import Flask, request
import os
import time, threading, schedule

# from dotenv import load_dotenv
# load_dotenv()

# TOKEN = os.getenv(API_KEY)
TOKEN = os.environ["API_KEY"]
bot = telebot.TeleBot(token=TOKEN)
server = Flask(__name__)

def findat(msg):
    # from a list of texts, it finds the one with the '@' sign
    for i in msg:
        if '@' in i:
            return i

@bot.message_handler(commands=['start']) # welcome message handler
def send_welcome(message):
    bot.reply_to(message, 'Hello, Welcome! type /help to get the commands')

@bot.message_handler(commands=['help']) # help message handler
def send_welcome(message):
    bot.reply_to(message, 'I will update the commands soon stay tune...')

@bot.message_handler(commands=['send']) # help message handler
def send_welcome(message):
    bot.reply_to(message, 'What do you want to send ?')

# code to schedule timer
def beep(chat_id) -> None:
    """Send the beep message."""
    bot.send_message(chat_id, text='Beep!')
@bot.message_handler(commands=['set'])
def set_timer(message):
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        sec = int(args[1])
        schedule.every(sec).second.do(beep, message.chat.id).tag(message.chat.id)
    else:
        bot.reply_to(message, 'Usages: /set <seconds>')
@bot.message_handler(commands=['unset'])
def unset_timer(message):
    schedule.clear(message.chat.id)

@bot.message_handler(func=lambda m: True)
def repeat(message):
    bot.send_message(message.chat.id, message.text)

@bot.message_handler(func=lambda msg: msg.text is not None and '@' in msg.text)
# lambda function finds messages with the '@' sign in them
# in case msg.text doesn't exist, the handler doesn't process it
def at_converter(message):
    texts = message.text.split()
    at_text = findat(texts)
    if at_text == '@': # in case it's just the '@', skip
        pass
    else:
        insta_link = "https://instagram.com/{}".format(at_text[1:])
        bot.reply_to(message, insta_link)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://telegrambot-bot1.herokuapp.com/' + TOKEN)
    return "Everything is working fine!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))