import telebot

bot = telebot.TeleBot("6379635079:AAHjOX9SuXHQrn-gmYQmkgBECAvG8lQ1COc", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN
cid=1691755707
mensaje_telegram='mensaje de prueba'
bot.send_message(cid, mensaje_telegram, parse_mode='html')