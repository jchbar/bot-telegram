# import telebot

# bot = telebot.TeleBot("6379635079:AAHjOX9SuXHQrn-gmYQmkgBECAvG8lQ1COc", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN
# cid=1691755707
# mensaje_telegram='mensaje de prueba'
# bot.send_message(cid, mensaje_telegram, parse_mode='html')

import requests
import time 
# import telegram
cid=1691755707
TOKEN = "6379635079:AAHjOX9SuXHQrn-gmYQmkgBECAvG8lQ1COc"
# url = f"https://api.telegram.org/bot{6379635079:AAHjOX9SuXHQrn-gmYQmkgBECAvG8lQ1COc}/getUpdates"
# print(requests.get(url).json())

# bot = telegram.Bot(TOKEN)
# bot.send_message(cid,"Lucky pepe")
# https://pypi.org/project/free-proxy/
from fp.fp import FreeProxy
proxy = FreeProxy(https=True).get()
print('proxy ',proxy)
# proxy = FreeProxy(country_id=['US', 'BR']).get()
# print('proxy country ',proxy)
# # country_id for US and GB You can set country_id to US and GB to get proxy from United States or United Kingdom. In that case proxies will be scrapped from https://www.us-proxy.org/ (US) or https://free-proxy-list.net/uk-proxy.html (GB) page. If there is no valid proxy from specified list check all countries
# proxy = FreeProxy(country_id=['US']).get()
# print('proxy us ',proxy)
# proxy = FreeProxy(country_id=['US']).get()
# print('proxy us ',proxy)

# proxy = FreeProxy(country_id=['GB']).get()
# print('proxy gb ',proxy)
# proxy = FreeProxy(country_id=['GB']).get()
# print('proxy gb ',proxy)

# timeout parameter Timeout is parameter for checking if proxy is valid. If test site doesn't respond in specified time script marks this proxy as invalid. Default timeout=0.5. You can change it by defining specified timeout eg. timeout=1.
# proxy = FreeProxy(timeout=1).get()
# rand parameter Shuffles proxy list from https://www.sslproxies.org/. Default rand=False and searches for working proxy from newest to oldest (as they are listed in https://www.sslproxies.org/).
# proxy = FreeProxy(rand=True).get()
# anonym parameter Return only those proxies that are marked as anonymous. Defaults to anonym=False
# proxy = FreeProxy(anonym=True).get()
# elite parameter Return only those proxies that are marked as 'elite proxy'. Defaults to elite=False.
# proxy = FreeProxy(elite=True).get()
# Note that elite proxies are anonymous at the same time, thus anonym=True automatically when elite=True.

# google parameter If True it returns only those proxies that are marked as google, if False - as no google. Defaults to google=None that returns all proxies.
# proxy = FreeProxy(google=True).get()
# https parameter If true it returns only those proxies that are marked as HTTPS. Defaults to https=False - i.e. HTTP proxy (for HTTP websites).

# Note that HTTPS proxy is for both HTTP and HTTPS websites.

# proxy = FreeProxy(https=True).get()
# You can combine parameters:

for i in range(6):
    proxy = FreeProxy(country_id=['US', 'BR'], timeout=0.3, rand=True, https=True).get()
    print('proxy country rand ',proxy)
    time.sleep(2)

for i in range(6):
    proxy = FreeProxy(timeout=0.3, rand=True, https=True).get()
    print('proxy  rand ',proxy)
    time.sleep(2)
