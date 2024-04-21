# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def main_():
#   return "flask instalado/running"

# if __name__ == "__main__": app.run();

# #  /usr /bin /env python3
from config import *
from flask import Flask, jsonify, make_response, request
# from telegramapi import TelegramApi
import telebot 
import time
import os
import sys
import re
import json

bot = telebot.TeleBot(TELEGRAM_API_TOKEN)
app = Flask(__name__)

@app.route("/")
def main_():
    return "flask instalado/running 4"

# telegramApi = TelegramApi(os.environ['TELEGRAM_API_TOKEN'])
# telegramApi = TelegramApi(TELEGRAM_API_TOKEN)
# print(telegramApi)

def logger(message):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    sys.stdout.write('{} | {}\n'.format(timestamp, message))


@app.route('/status', methods=['GET'])
def get_status():
    return 'Up and running', 201
@app.route('/set_webhook', methods=['GET','POST'])
def set_webhook():
    bot.remove_webhook()
    # s = bot.set_webhook(url="{BASE_URI}{WEBHOOK}".format(URL=BASE_URI,HOOK=TELEGRAM_API_TOKEN))
    # s = bot.set_webhook(url="{BASE_URI}{WEBHOOK}")
    s = bot.set_webhook(url="https://pruebaocr.cappoucla.org.ve/")
    time.sleep(1)
    if s:
        return 'set_webhook Ok', 201
    else:
        return 'set_webhook NoOk', 201

# 
@app.route('/',methods=['POST'])
def webhook():
    if request.headers.get("content-type") == "application/json":
        update = bot.types.Update.de_json(request.stream.read().decode('utf-8'))
        bot.process_new_update([update])
        return "Ok",200

@bot.message_handler(command=['start'])
def cmd_start(message):
    bot.send_message(message.chat.id,"Hola",parse_mode="html")

@bot.message_handler(command=['text'])
def bot_texto(message):
    bot.send_message(message.chat.id,"He recibido "+message.text,parse_mode="html")


# 

# @app.route('/webhook/<webhook>', methods=['GET', 'POST'])
# def get_webhook(webhook):
#     logger(webhook)
#     if os.environ['WEBHOOK'] != webhook:
#         return 'KO', 404
#     try:
#         if request.method == 'GET' or not request.json:
#             return 'OK', 200
#     except Exception:
#         return 'OK', 200
#     payload = request.json
#     logger(json.dumps(payload, indent=4, sort_keys=True))
#     return 'OK', 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
