__version__ = "1.1.0"
__date__ = '2024/04/10'
__author__ = "Juan C Hernandez B"

'''
python3 -m venv bot-telegram
source bin/activate

pip install pytelegrambotapi
pip install requests
pip install pyngrok
pip install flask
# pip install waitress
pip install py-mon
pip install load_dotenv
pip install pytesseract

    pymon app.py
'''


# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def main_():
#   return "flask instalado/running"

# if __name__ == "__main__": app.run();

# #  /usr /bin /env python3
# from config import *
from flask import Flask, jsonify, make_response, request, Response
# from pyngrok import ngrok, conf
# from telegramapi import TelegramApi
import telebot 
import time
import os
import sys
import random, re
import json
import requests
# from waitress import serve
import threading
from telebot.types import ReplyKeyboardMarkup, ForceReply, ReplyKeyboardRemove
# import logging
import pytesseract
from PIL import Image
from dotenv import load_dotenv


# bot = telebot.TeleBot(TELEGRAM_API_TOKEN)
app = Flask(__name__)

# import logging
# logger = logging.getLogger(__name__)
# logging.basicConfig(filename='registro.log',  level=logging.INFO)
# # encoding='utf-8',
# logger.debug('This message should go to the log file')
# logger.info('So should this')
# logger.warning('And this, too')
# logger.error('And non-ASCII stuff, too, like Øresund and Malmö')
def bitacora(message, file_name='registro.log'):
    # with open(file_name, 'a') as f:
        # json.dump(data, f, indent=4)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    sys.stdout.write('{} | {}\n'.format(timestamp, message))
    file=open(file_name,'a')
    file.write('{} | {}\n'.format(timestamp, message))
    file.close()

load_dotenv()
SERVER_LOCAL    = os.getenv('SERVER_LOCAL', 'No definido SERVER_LOCAL')
SERVER_LOCAL    = True if SERVER_LOCAL=='1' else False
if (SERVER_LOCAL == True):
    TELEGRAM_API_TOKEN  = os.getenv('TELEGRAM_API_TOKEN_TEST', 'No definido SERVER_LOCAL')
    url                 = os.getenv('SERVER_NGROK', 'No definido SERVER_LOCAL')
    servidor            = os.getenv('SERVER_NGROK', 'No definido SERVER_LOCAL')
    PORT                = os.getenv('PORT_TEST', 'No definido SERVER_LOCAL')
    print('Seleccionado SERVER_LOCAL')
    bitacora('Seleccionado SERVER_LOCAL '+url + servidor + str(PORT))
else:
    TELEGRAM_API_TOKEN  = os.getenv('TELEGRAM_API_TOKEN_REAL', 'No definido SERVER_LOCAL')
    url                 = os.getenv('SERVER_REAL', 'No definido SERVER_LOCAL')
    servidor            = os.getenv('SERVER_REAL', 'No definido SERVER_LOCAL')
    PORT                = os.getenv('PORT_REAL', 'No definido SERVER_LOCAL')
    print('Seleccionado SERVER_REAL')
    bitacora('Seleccionado SERVER_REAL '+url + servidor + str(PORT)) 

bot = telebot.TeleBot(TELEGRAM_API_TOKEN)
BOT_COMMANDS= [
    {"command":"iniciar", "description":"Iniciar el Bot"},
    {"command":"identificarme","description":"Iniciar sesion de datos"},
    {"command":"ayuda", "description":"Muestra los comandos a utilizar"},
    # {"command":"progreso", "description":"Probar barra de progreso"},
    # {"command":"responderbien", "description":"Probar datos fijos y respuesta buena json"},
    # {"command":"respondermal", "description":"Probar datos fijos y respuesta errado json"},
    # {"command":"ocr", "description":"Probar ocr"},
    # {"command":"procesar_imagen", "description":"Probar obtener images y procesar datos"},
]
BOT_COMMANDS_SESION= [
    {"command":"disponibilidad", "description":"Mostrar mi disponibilidad"},
    {"command":"saldo_haberes","description":"Resumen de mis haberes"},
    {"command":"saldo_prestamos","description":"Resumen de mis prestamos"},
    {"command":"pago","description":"Informar pago"},
    {"command":"regresar", "description":"Menu Anterior"},
    # {"command":"progreso", "description":"Probar barra de progreso"},
    # {"command":"responderbien", "description":"Probar datos fijos y respuesta buena json"},
    # {"command":"respondermal", "description":"Probar datos fijos y respuesta errado json"},
    # {"command":"ocr", "description":"Probar ocr"},
    # {"command":"procesar_imagen", "description":"Probar obtener images y procesar datos"},
]
este_bot = ' para Consultas de Caja de Ahorro  '
version_bot = __version__
# txt_pregunta_cedula = "Cuál es su número de cédula"
# txt_pregunta_codigo = "Cuál es el código de asociado"
txt_pregunta_cedula = "Cual es su numero de cedula"
txt_pregunta_codigo = "Cual es el codigo de asociado"
txt_si_disponibilidad = "Si, es correcto"
txt_no_disponibilidad = "No, no es correcto"
datos_consulta = {
    "chat_id":0,
    "cedula":"",
    "codigo":"",
    "id_msg_cedula":0,
    "id_msg_codigo":0
}
arreglo_botones = []

# logger = logging.getLogger(__name__)
# logging.basicConfig(filename="logger.log",  level=logging.DEBUG)
# # encoding="utf-8",

def write_json(data, file_name='response.json'):
    with open(file_name, 'a') as f:
        json.dump(data, f, indent=4)
        # , ensure_ascii=False)
    bitacora('escribi en archivo json ')

# 
# https://api.telegram.org/bot6897485406:AAE116uTF5894G5aN0wJZ8UmfHIwRLbAnFc/getMe
# https://api.telegram.org/bot6897485406:AAE116uTF5894G5aN0wJZ8UmfHIwRLbAnFc/getUpdates
# https://api.telegram.org/bot6897485406:AAE116uTF5894G5aN0wJZ8UmfHIwRLbAnFc/setWebhook?url=https://pruebaocr.cappoucla.org.ve
# https://api.telegram.org/bot6897485406:AAE116uTF5894G5aN0wJZ8UmfHIwRLbAnFc/deleteWebhook
# https://api.telegram.org/6379635079:AAHjOX9SuXHQrn-gmYQmkgBECAvG8lQ1COc/setWebhook?url=https://badly-exact-skink.ngrok-free.app
# https://api.telegram.org/bot6897485406:AAE116uTF5894G5aN0wJZ8UmfHIwRLbAnFc/
# https://pytba.readthedocs.io/en/latest/
# 

def deleteWebhook():
    url = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/deleteWebhook'
    payload = {
        # 'chat_id':chat_id,
        # 'action':mostrar
    }
    r = requests.post(url, json=payload)
    bitacora('deleteWebhook api')
    return r

def setWebhook(url):
    url = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/setWebhook?url='+url
    payload = {
        # 'url':url,
        # 'action':mostrar
    }
    r = requests.post(url) #, json=payload)
    print ('setWebhook',url)
    bitacora('setWebhook api')
    return r


def sendChatAction(chat_id, tipo:'texto'):
    # switcher = {
    #     'texto' :   'typing',
    #     'foto'  :   'upload_photo',
    #     'video' :   'upload_video',
    #     'voz'   :   'upload_voice',
    #     'documento':'upload_document',
    #     'sticker':  'choose_sticker',
    #     'ubicacion' : 'find_location'
    # }
    # mostrar = switcher.get(argument, tipo)
    # funcion en python 3.10
    # match tipo:
    #     case  'texto':
    #         mostrar='typing'
    #     case 'foto'  :   
    #         mostrar='upload_photo'
    #     case 'video' :   
    #         mostrar='upload_video'
    #     case 'voz'   :   
    #         mostrar='upload_voice'
    #     case 'documento':
    #         mostrar='upload_document'
    #     case 'sticker':  
    #         mostrar='choose_sticker'
    #     case 'ubicacion' : 
    #         mostrar='find_location'
    if tipo == 'texto':
        mostrar='typing'
    elif tipo == 'foto':   
        mostrar='upload_photo'
    elif tipo == 'video':   
        mostrar='upload_video'
    elif tipo ==  'voz':   
        mostrar='upload_voice'
    elif tipo == 'documento':
        mostrar='upload_document'
    elif tipo == 'sticker':  
        mostrar='choose_sticker'
    elif tipo ==  'ubicacion' : 
        mostrar='find_location'
    else:
        mostrar = 'typing'
    url = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendChatAction'
    payload = {
        'chat_id':chat_id,
        'action':mostrar
    }
    r = requests.post(url, json=payload)
    bitacora('sendChatAction '+mostrar)
    return r


# def send_message(chat_id, text='nothing'):
#     sendChatAction(chat_id,'text')
#     url = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage'
#     payload = {
#         'chat_id':chat_id,
#         'text':text,
#         "parse_mode":"html"
#     }
#     r = requests.post(url, json=payload)
#     bitacora('send_message api ')
#     return r


# def existe_comando(txt_comando):
#     existe = False
#     for comando in BOT_COMMANDS:
#         if comando['command'] == txt_comando:
#             existe = True
#             break
#     return existe

# def preguntar(chat_id, texto):
#     sendChatAction(chat_id,'text')
#     url = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/ForceReply'
#     payload = {
#         'chat_id':chat_id,
#         'text':texto,
#         "parse_mode":"html"
#     }
#     r = requests.post(url, json=payload)
#     return r

def definir_comandos(BOT_COMMANDS):
    bitacora('entre definir_comandos')
    # BOT_COMMANDS= [{"command":"Iniciar", "description":"Iniciar el Bot"},{"command":"Disponibilidad","description":"Obtener mi Disponibilidad"}]
    # url = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/setMyCommands'
    # payload = {
    #     'chat_id':chat_id,
    #     'action':mostrar
    # }
    # r = requests.post(url, json=payload)
    send_text = url + '?commands=' + str(json.dumps(BOT_COMMANDS) ) 
    r  = requests.get(send_text)
    bitacora('sali definir_comandos')
    return r

def botones_session(msg):
    if (datos_consulta['cedula'] == '' or datos_consulta['codigo']==''):
        bot.send_message(chat_id, 'Lo siento... \nAlgo malo ha ocurrido con los datos para obtener sesion, <b>revise sus datos e intente nuevamente</b>',parse_mode='html')
        # iniciar()
        identificarme(msg)

    chat_id=obtener_chat_id(msg)
    sendChatAction(chat_id,'texto')

    # validar que tenga informacion de cedula y codigo 
    # la funcion disponibilidad cambiarla para no pedir los datos

    txt_Disponibilidad  = 'Disponibilidad'
    txt_haberes         = 'Saldo Haberes'
    txt_prestamos       = 'Saldo Prestamos'
    txt_pagos           = 'Informar Pago'
    txt_salir           = 'Cerrar Sesion'

    # print('arreglo_botones antes')
    # print(arreglo_botones)
    if len(arreglo_botones) < 1:
        arreglo_botones.append(txt_Disponibilidad)
        arreglo_botones.append(txt_haberes)
        arreglo_botones.append(txt_prestamos)
        arreglo_botones.append(txt_pagos)
        arreglo_botones.append(txt_salir)
    # print('arreglo_botones despues')
    # print(arreglo_botones)

    botones = ReplyKeyboardMarkup(
        one_time_keyboard=True, 
        input_field_placeholder="Puede utilizar los Botones o el menu para seleccionar", 
        resize_keyboard=True)
    # markup.add(txt_Disponibilidad, txt_haberes, txt_prestamos, txt_pagos, txt_salir)
    botones.row(txt_Disponibilidad)
    botones.row(txt_haberes, txt_prestamos)
    botones.row(txt_pagos)
    botones.row(txt_salir)
    msg = bot.send_message(chat_id, 'Opciones disponibles ', reply_markup=botones)
    definir_comandos(BOT_COMMANDS)


def botones_inicio(msg):
    chat_id=obtener_chat_id(msg)
    sendChatAction(chat_id,'texto')
    # txt_inicio      = 'Iniciar'
    # txt_identificar = 'identificarme'
    # txt_ayuda       = 'Ayuda'
    # botones = ReplyKeyboardMarkup(
    #     one_time_keyboard=True, 
    #     input_field_placeholder="Puede utilizar los Botones o el menu para seleccionar", 
    #     resize_keyboard=True)
    # # markup.add(txt_Disponibilidad, txt_haberes, txt_prestamos, txt_pagos, txt_salir)
    # botones.row(txt_inicio, txt_identificar, txt_ayuda)
    # msg = bot.send_message(chat_id, 'Opciones disponibles ', reply_markup=botones)
    definir_comandos(BOT_COMMANDS_SESION)

def menu_anterior(msg):
    botones_inicio(BOT_COMMANDS)

def ayuda(msg):
    chat_id=obtener_chat_id(msg)
    print('estoy en ayuda')
    sendChatAction(chat_id,'texto')
    texto =  "<b>Commandos que pueden utilizarse</b>\n" \
            "/iniciar - <b>Inicia el servicio de bot</b>\n" \
            "/identificarme - <b>Iniciar sesion de datos</b>\n" \
            "/ayuda - <b>Este mensaje</b>"
            # "/disponibilidad - <b>Obtener su disponibilidad</b>\n" \
    markup = ReplyKeyboardRemove()
    bot.send_message(chat_id, texto, parse_mode="html",reply_markup=markup)
    botones_inicio(msg)
    bitacora('funcion ayuda ')


def iniciar(msg):
    # print('estoy en iniciar')
    chat_id=obtener_chat_id(msg)
    sendChatAction(chat_id,'texto')
    markup = ReplyKeyboardRemove()
    cuento = "<b><i>Bienvenido(a) al Bot "+este_bot + version_bot + '</i></b>\n\n'
    cuento += 'Utilizando tecla <b>/</b> puede obtener los comandos disponibles o bien si le aparece el menú también puede utilizarlo\n'
    cuento += '\nSi desea obtener la disponibilidad debe seguir los pasos indicados, le envio la imagen de referencia'
    bot.send_message(chat_id, cuento, parse_mode="html", reply_markup=markup)
    botones_inicio(msg)

    # sendChatAction(chat_id,'foto')
    # foto = open('./images/ejemplo.jpeg', 'rb')
    # bot.send_photo(chat_id, foto, 'Ejemplo para obtener su disponibilidad')
    bitacora('funcion iniciar ')


def eliminar_msg(chat_id, id_msg):
    bitacora('entre eliminar_msg ')
    try:
        bot.delete_message(chat_id, id_msg)
    except Exception as error:
        print('no pude eliminar_msg',chat_id,id_msg,error)
    bitacora('sali eliminar_msg ')

def confirmar_datos(message):
    bitacora('entre confirmar_datos ')
    try:
        print('estoy en confirmar_datos')
        # print(message)
        print(datos_consulta)
        chat_id = obtener_chat_id(message)
        texto = obtener_chat_text(message)
        if not texto.isdigit():
            respuesta = ForceReply()
            respuesta = bot.send_message(chat_id, 'Para poder indicarte tu disponibilidad debes indicar tambien el codigo de asociado ')
        else:
            cedula = datos_consulta['cedula']
            codigo = datos_consulta['codigo']
            id_msg_ced = datos_consulta['id_msg_cedula']
            id_msg_cod = datos_consulta['id_msg_codigo']
            if (codigo == '') or (cedula == ''):
                bot.send_message(chat_id, 'Lo siento... \nAlgo malo ha ocurrido con los datos, <b>revise sus datos e intente nuevamente</b>',parse_mode='html')
                eliminar_msg(chat_id, id_msg_ced)
                eliminar_msg(chat_id, id_msg_cod)
            else:
                codigo = texto
                if consultardatos(message, chat_id, 0):
                    botones_session(message)
                else:
                    markup = ReplyKeyboardRemove()
                    bot.send_message(chat_id, 
                        'Tuvimos inconveniente para iniciar sesion',
                        parse_mode='html',
                        reply_markup=markup)
                # responder_disponibilidad(chat_id)
                # botones_session(message)
                # markup = ReplyKeyboardMarkup(
                #     one_time_keyboard=True, 
                #     input_field_placeholder="Los datos suministrados son correctos?", 
                #     resize_keyboard=True)
                # markup.add(txt_si_disponibilidad,txt_no_disponibilidad)
                # msg = bot.send_message(chat_id, 'Disponibilidad para '+cedula+' y '+codigo, reply_markup=markup)
                # bot.register_next_step_handler(msg, preguntar_codigo)
    except Exception as error:
        print('error en confirmar_datos',error)
        bot.send_message(chat_id, 'Lo siento... \nAlgo malo ha ocurrido con los datos, <b>revise sus datos e intente nuevamente</b>',parse_mode='html')
    bitacora('sali confirmar_datos ')


def preguntar_codigo(message):
    bitacora('entre preguntar_codigo ')
    print(message)
    chat_id = obtener_chat_id(message)
    texto = obtener_chat_text(message)
    # print('estoy en preguntar_codigo')
    # if not message.text.isdigit():
    if not texto.isdigit():
        respuesta = ForceReply()
        respuesta = bot.send_message(chat_id, 'Para poder indicarte tu disponibilidad debes indicar el numero de la cedula ')
    else:
        cedula = texto
        respuesta = ForceReply()
        # bot.send_message(chat_id, 'El número de cedula es '+cedula, parse_mode='html')
        respuesta = bot.send_message(chat_id, txt_pregunta_codigo,reply_markup=respuesta)
        # print(respuesta)
        bot.register_next_step_handler(respuesta, responder_disponibilidad)
    bitacora('sali preguntar_codigo ')

def consultardatos(msg, cid, mid):
    bitacora('entre consultardatos')
    try:
        # cid=obtener_chat_id(msg)
        # mid = barra_progreso(0,'Estableciendo conexion a datos',cid)
        # print('mid responder_disponibilidad',mid)
        cedula = datos_consulta['cedula']
        codigo = datos_consulta['codigo']
        respuesta = solicitar_informacion(cedula, codigo, cid, mid, 'obtenerdatosB')
        write_json(respuesta, 'telegram_request.json')
        return respuesta['respuesta'], respuesta
    except Exception as error:
        print('error en consultardatos',error)
    bitacora('sali consultardatos  ')
    return 'NoOk', []


def saldohaberes(msg):
    cid=obtener_chat_id(msg)
    bitacora('entre disponibilidad ')
    sendChatAction(cid,'texto')
    mid = barra_progreso(0,'Estableciendo conexion a datos',cid)
    respuesta, resultado = consultardatos(msg, cid, mid)
    if respuesta =='Ok':
        respuesta=resultado
        sendChatAction(cid,'texto')
        barra_progreso(numAzar(45,55),'Procesando informacion',cid, mid)
        time.sleep(0.5)
        sendChatAction(cid,'texto')
        barra_progreso(numAzar(85,95),'Entregando informacion',cid, mid)
        time.sleep(0.5)
        barra_progreso(100,'Preparando la entrega de informacion',cid, mid)
        socio = respuesta['datos']
        # cuento = "Estimado(a) Socio(a):<b><span class='tg-spoiler'>"+socio['nombre']+'</span><b>\n'
        cuento = "Estimado(a) Socio(a):<b>"+socio['nombre']+'</b>\n'
        cuento += 'Datos actualizados el '+respuesta['actualizacion']['fechaactdatos']+'\n'
        cuento += 'Ahorros Socio al '+socio['uas']+': <b>'+str(socio['hab_f_prof'])+'</b>\n'
        cuento += 'Aporte Patronal al '+socio['uap']+': <b>'+str(socio['hab_f_empr'])+'</b>\n'
        # cuento += 'Ahorros Socio al '+socio['uas']+': <b>'+socio['hab_f_prof']+'</b>\n'
        cuento += '\nPara mayor informacion puede consultar el Estado de Cuenta en '
        cuento += '<a href="https://estadodecuenta.cappoucla.org.ve">Estado de Cuenta</a>\n'
        cuento += '\nIgualmente lo invitamos a visitar regularmente nuestro sitio web '
        # cuento += '<a href="https://cappoucla.org.ve">cappoucla.org.ve</a>\n'
        cuento += '<a href="'+SITIOWEB+'">'+SITIOWEB+'</a>\n'
        sendChatAction(cid,'texto')
        bot.send_message(cid, cuento, parse_mode='html')
    else:
        barra_progreso(100,'Preparando entrega de informacion',cid, mid)
        markup = ReplyKeyboardRemove()
        bot.send_message(cid, '<b>No he podido obtener la informacion solicitada, revise los datos e intente de nuevo</b>', parse_mode='html')
        bot.send_message(cid, 
                '<b>Si no esta afiliado a la institucion puede visitar </b><a href="'+SITIOWEB+'">'+SITIOWEB+'</a> para su inscripcion', 
                parse_mode='html', 
                reply_markup=markup)
    bitacora('sali disponibilidad ')


def disponibilidad(msg):
    # version anterior 
    # chat_id=obtener_chat_id(msg)
    # bitacora('entre disponibilidad ')
    # print('estoy en disponibilidad')
    # sendChatAction(chat_id,'texto')
    # # botones = ReplyKeyboardRemove()
    # # respuesta = bot.send_message(chat_id, '',reply_markup=botones)
    # markup = ForceReply()
    # respuesta = bot.send_message(chat_id, txt_pregunta_cedula,reply_markup = markup, parse_mode='html')
    # # print(respuesta)
    # bot.register_next_step_handler(respuesta, preguntar_codigo)

    chat_id=obtener_chat_id(msg)
    bitacora('entre disponibilidad ')
    sendChatAction(chat_id,'texto')
    responder_disponibilidad(obtener_chat_id(msg))
    bitacora('sali disponibilidad ')

def clave_en_lista(msg, buscar):
    lista = list(msg.keys())
    existe = False
    for llave in lista:
        if llave==buscar:
            existe=True
            break
    return existe


def parse_message(message):
    bitacora('entre parse_message ')
    chat_id = message['message']['chat']['id']
    comando = respuesta = mensaje = False
    if ('text' in message['message']):
        txt = message['message']['text']
        txt = txt.lower()

        if (clave_en_lista(message['message'],'entities')):
            if (clave_en_lista(message['message']['entities'][0],'type')):
                # if (clave_en_lista(message['message']['entities'][0]['type'],'bot_command')):
                comando = True
                txt = txt.strip()
                if txt and (txt.startswith('/')):
                    tamano = len(txt)
                    txt = txt[1:tamano]
                print ('es un comando ')
        else:
            if (clave_en_lista(message['message'],'reply_to_message')):
                print('es una respuesta')
                respuesta = True
            else:
                mensaje = True
                print('mensaje normal')

        print ('resultado comando ',comando, 'respuesta ', respuesta, ' mensaje ',mensaje)
        bitacora('sali parse_message ')
        return chat_id, txt, comando,respuesta, mensaje 
    elif ('photo' in message['message']):
        comando = True
        mensaje = False
        txt = 'procesar_imagen' 
        print('recibi una imagen')

    print('sali de parse_message')
    return chat_id, txt, comando,respuesta, mensaje 

    '''
    if "/launches" in message_text:
        launches = libs.upcoming_launches(6)
        text = ""
        for launch in launches:
            if launch["tbd"]:
                tbd = "(<b>TBD</b>)"
            else:
                tbd = ""
            text += "<b>{}</b>\n{}\n<i>{}</i> {}\n\n".format(launch["name"], launch["location"], launch["net"], tbd)
        return text
    elif "/weather" in message_text:
        return "weather"
    elif "/money" in message_text:
        return "money"
    elif "/hello" in message_text:
        return "Hello {}!".format(first_name)
    elif "/help" in message_text:
        return "<b>Commands</b>\n" \
               "/launches - <b>Upcoming Launches</b>\n" \
               "/weather - <b>Weather on your place</b>\n" \
               "/money - <b>Exchange Rates</b>\n" \
               "/hello - <b>Hello test message</b>\n" \
               "/help - <b>This message</b>"
    else:
        return None
    '''

def obtener_chat_id(msg):
    return msg["message"]["chat"]["id"]

def obtener_msg_id(msg):
    return msg["message"]["reply_to_message"]["message_id"]
    # .encode('utf8')

def obtener_chat_text(msg):
    return msg["message"]["text"]
    # .encode('utf8')

def obtener_pregunta_hecha(msg):
    return msg["message"]["reply_to_message"]['text']

def obtener_chat_foto(msg):
    maximo = (1024*5)*1024
    print('entrando en obtener_chat_foto')
    foto = msg["message"]["photo"]
    # print(foto)
    foto_resultado = ''
    foto_buena = False 
    for lafoto in foto:
        # print(lafoto['file_id'])
        if int(lafoto['file_size']) < maximo:
            foto_resultado = lafoto
            foto_buena = True

    print('saliendo en obtener_chat_foto')
    return foto_resultado, foto_buena

def cursor_arriba(n=1):
    print(f'\33[{n}A',end='')

def barra_progreso(porcentaje, texto="", cid=None, mid=None, terminal=False):
    bitacora('entre barra_progreso  '+str(porcentaje))
    try:
        t, no, si = ('|','-','#')
        if terminal:
            blanco = "\33[1:37m"
            amarillo = "\33[1:33m"
            gris = "\33[0:33m"
            gris2 = "\33[0:90m"
            ancho = os.get_terminal_size().columns -20
            cuadros_si = porcentaje * ancho // 100
            cuadros_no = ancho - cuadros_si
            barra_terminal = f'\33[K{blanco}|{amarillo}{t*cuadros_si}{gris2}{t*cuadros_no}{blanco}|{porcentaje:>3}{gris}'
            texto_terminal = f'\33[K{amarillo}] {texto}\n{barra_terminal}'
            print(texto_terminal)
            if porcentaje < 100:
                cursor_arriba(2)
            elif porcentaje > 100:
                cursor_arriba(2)
                print("\33[K")
                print("\33[K")
                cursor_arriba(2)
        if cid:
            cuadros_si = porcentaje // 10
            cuadros_no = 10 - cuadros_si
            barra_telegram = si*cuadros_si + no*cuadros_no
            mensaje_telegram = f'{texto}\n{barra_telegram} <code>{porcentaje:>3}%</code>'
            if not mid:
                msg = bot.send_message(cid, mensaje_telegram, parse_mode='html')
                return msg.message_id
            else:
                if porcentaje < 100:
                    bot.edit_message_text(mensaje_telegram, cid, mid, parse_mode='html')
                    return 
                elif porcentaje == 100:
                    time.sleep(1)
                    eliminar_msg(cid, mid)
                    return
    except Exception as error:
        print('error en barra_progreso',error)
    bitacora('sali barra_progreso  ')

def numAzar(inicio=0, fin=100):
    bitacora('entre numAzar  ')
    azar = random.randint(inicio,fin)
    bitacora('entre numAzar  '+str(azar))
    return azar


def progreso(cid):
    # cid = obtener_chat_id(msg)
    bitacora('entre progreso  ')
    mid = barra_progreso(0,'iniciando',cid)
    time.sleep(2)
    barra_progreso(numAzar(18,23),'conectando',cid, mid)
    time.sleep(2)
    barra_progreso(numAzar(45,55),'obteniendo datos',cid, mid)
    time.sleep(2)
    barra_progreso(numAzar(70,80),'procesando datos',cid, mid)
    time.sleep(2)
    barra_progreso(100,'finalizando',cid, mid)
    bitacora('sali progreso  ')

# enviarEmail
def solicitar_informacion(cedula, codigo, cid, mid, comando):
    bitacora('entre solicitar_informacion  ')
    try:
        # print('cid',cid,'mid',mid)
        barra_progreso(numAzar(18,25),'Obteniendo informacion API',cid, mid)
        new_data = {
            "cedula": cedula,
            "codigo": codigo,
        }
        url_post = URL_API+comando
        # print(url_post, new_data)
        post_response = requests.post(url_post, json=new_data)
        # Print the response
        post_response_json = post_response.json()
        # print(post_response_json)
        return post_response_json
    except Exception as error:
        print('error en solicitar_informacion',error)
        return {
            "respuesta": "NoOk"
        }
    bitacora('sali solicitar_informacion  ')


def responder_disponibilidad(cid):
    bitacora('entre responder_disponibilidad  ')
    try:
        mid = barra_progreso(0,'Estableciendo conexion a datos',cid)
        # print('mid responder_disponibilidad',mid)
        cedula = datos_consulta['cedula']
        codigo = datos_consulta['codigo']
        respuesta = solicitar_informacion(cedula, codigo, cid, mid, 'obtenerdatosB')
        write_json(respuesta, 'telegram_request.json')
        # write_json(respuesta, 'telegram_request.json')
        if respuesta['respuesta'] =='Ok':
            sendChatAction(cid,'texto')
            barra_progreso(numAzar(45,55),'Procesando informacion',cid, mid)
            time.sleep(0.5)
            sendChatAction(cid,'texto')
            barra_progreso(numAzar(85,95),'Entregando informacion',cid, mid)
            time.sleep(0.5)
            barra_progreso(100,'Preparando entrega de informacion',cid, mid)
            socio = respuesta['datos']
            # cuento = "Estimado(a) Socio(a):<b><span class='tg-spoiler'>"+socio['nombre']+'</span><b>\n'
            cuento = "Estimado(a) Socio(a):<b>"+socio['nombre']+'</b>\n'
            cuento += 'Su disponibilidad es de <b>'+str(respuesta['disponibilidad'])+'</b>\n'
            if (respuesta['tsuspension'] > 0):
                cuento += 'Tiene un saldo pendiente de '+str(respuesta['tsuspension'])+'\n'
            cuento += 'Datos actualizados el '+respuesta['actualizacion']['fechaactdatos']+'\n'
            cuento += '\nPara mayor informacion puede consultar el Estado de Cuenta en '
            cuento += '<a href="https://estadodecuenta.cappoucla.org.ve">Estado de Cuenta</a>\n'
            cuento += '\nIgualmente lo invitamos a visitar regularmente nuestro sitio web '
            # cuento += '<a href="https://cappoucla.org.ve">cappoucla.org.ve</a>\n'
            cuento += '<a href="'+SITIOWEB+'">'+SITIOWEB+'</a>\n'
            sendChatAction(cid,'texto')
            bot.send_message(cid, cuento, parse_mode='html')
        else:
            barra_progreso(100,'Preparando entrega de informacion',cid, mid)
            bot.send_message(cid, '<b>No he podido obtener la informacion solicitada, revise los datos e intente de nuevo</b>', parse_mode='html')
            markup = ReplyKeyboardRemove()
            bot.send_message(
                cid, 
                '<b>Si no esta afiliado a la institucion puede visitar </b><a href="'+SITIOWEB+'">'+SITIOWEB+'</a> para su inscripcion', 
                parse_mode='html',
                reply_markup=markup)
    except Exception as error:
        print('error en responder_disponibilidad',error)
    bitacora('sali responder_disponibilidad  ')

def responderbien(msg):
    cid=obtener_chat_id(msg)
    datos_consulta['cedula']='09377388'
    datos_consulta['codigo']='00914'
    responder_disponibilidad(cid)

def respondermal(msg):
    cid=obtener_chat_id(msg)
    datos_consulta['cedula']='0937738'
    datos_consulta['codigo']='00914'
    responder_disponibilidad(cid)

def identificarme(msg):
    chat_id=obtener_chat_id(msg)
    bitacora('entre identificarme ')
    sendChatAction(chat_id,'texto')
    # botones = ReplyKeyboardRemove()
    # respuesta = bot.send_message(chat_id, '',reply_markup=botones)
    markup = ForceReply()
    respuesta = bot.send_message(chat_id, txt_pregunta_cedula,reply_markup = markup, parse_mode='html')
    # print(respuesta)
    bot.register_next_step_handler(respuesta, preguntar_codigo)
    bitacora('sali identificarme ')

def continuar_identificacion(msg):
    bitacora('entre continuar identificarme  ')
    try:
        pregunta_hecha = obtener_pregunta_hecha(msg)
        chat_id = obtener_chat_id(msg)
        if pregunta_hecha.lower() == txt_pregunta_cedula.lower():
            texto = obtener_chat_text(msg)
            if not texto.isdigit(): # preguntar codigo
                disponibilidad(obtener_chat_id(msg))
            else:
                texto = texto.zfill(8)
                datos_consulta['cedula']=texto
                datos_consulta['id_msg_cedula']=obtener_msg_id(msg)
                print('entre cedula es digito ')
                preguntar_codigo(msg)
        if pregunta_hecha.lower() == txt_pregunta_codigo.lower():
            texto = obtener_chat_text(msg)
            if not texto.isdigit(): # preguntar codigo
                preguntar_codigo(msg)
            else:
                texto = texto.zfill(5)
                datos_consulta['codigo']=texto
                datos_consulta['id_msg_codigo']=obtener_msg_id(msg)
                if consultardatos(msg, chat_id, 0):
                    botones_session(msg)
                else:
                    markup = ReplyKeyboardRemove()
                    bot.send_message(chat_id, 
                        'Tuvimos inconveniente para iniciar sesion',
                        parse_mode='html',
                        reply_markup=markup)

                # confirmar_datos(msg)
                # send_message(chat_id, 'mostrar botones')
    except Exception as error:
        print('error en procesar_respuesta',error)
        bot.send_message(chat_id, 'Escribiste algo que no he entendido que quieres decir con <b><u>'+txt+'</u></b>\n Puedes utilizar <b>/</b> para ver los comandos o para obtener <b>/ayuda</b> ',parse_mode='html')
        iniciar()
    bitacora('sali continuar identificarme  ')


def procesar_respuesta(msg):
    bitacora('entre procesar_respuesta  ')
    try:
        pregunta_hecha = obtener_pregunta_hecha(msg)
        chat_id = obtener_chat_id(msg)
        print('la pregunta hecha',pregunta_hecha, txt_pregunta_cedula.lower())
        if pregunta_hecha.lower() == txt_pregunta_cedula.lower():
            texto = obtener_chat_text(msg)
            if not texto.isdigit(): # preguntar codigo
                disponibilidad(obtener_chat_id(msg))
            else:
                texto = texto.zfill(8)
                datos_consulta['cedula']=texto
                datos_consulta['id_msg_cedula']=obtener_msg_id(msg)
                print('entre cedula es digito ')
                preguntar_codigo(msg)
        if pregunta_hecha.lower() == txt_pregunta_codigo.lower():
            texto = obtener_chat_text(msg)
            if not texto.isdigit(): # preguntar codigo
                preguntar_codigo(msg)
            else:
                texto = texto.zfill(5)
                datos_consulta['codigo']=texto
                datos_consulta['id_msg_codigo']=obtener_msg_id(msg)
                confirmar_datos(msg)
        # if pregunta_hecha.lower() == txt_si_disponibilidad.lower():
        #     responder_disponibilidad(msg)
    except Exception as error:
        print('error en procesar_respuesta',error)
        bot.send_message(chat_id, 'Escribiste algo que no he entendido que quieres decir con <b><u>'+txt+'</u></b>\n Puedes utilizar <b>/</b> para ver los comandos o para obtener <b>/ayuda</b> ',parse_mode='html')
        iniciar()
    bitacora('sali procesar_respuesta  ')


    # bot.send_message(obtener_chat_id(msg),'estoy en procesar_respuesta')


def recibir_msg(app):
    bitacora('entre recibir_msg')
    print(threading.current_thread().getName())
        # if SERVER_LOCAL==True:
        #     conf.get_default().config_path = './config_ngrok.yml'
        #     # conf.get_default.region='us'
        #     # ngrok.set_auth_token(NGROK_TOKEN)
        #     # ngrok_url = ngrok.connect()
        #     # # 6000, bind_tls=False).public_url
        #     # print('Url Nrgrok ',ngrok_url)
        #     print('desactivando Webhook')
        #     deleteWebhook()
        #     time.sleep(1)
        #     # ngrok http --domain=badly-exact-skink.ngrok-free.app 5000
        #     # servidor_ngrok=SERVER_NGROK
        # #     print('asignando Webhook', setWebhook(servidor_ngrok))
        # # else:
        #     print('asignando Webhook', setWebhook(servidor))

        # if SERVER_LOCAL==False:
        # try:
    if not SERVER_LOCAL:
        print('desactivando Webhook')
        deleteWebhook()
        time.sleep(1)
        print('asignando Webhook', setWebhook(servidor))
        #     return True
        # except Exception as error:
        #     print('fallo inicio configuracion bot ',error)
        #     return False
    bitacora('sali recibir_msg')



# def contar():
#     contador = 0
#     while contador<100:
#         contador+=1
#         print('Hilo:', 
#               threading.current_thread().getName(), 
#               'con identificador:', 
#               threading.current_thread().ident,
#               'Contador:', contador)

def evaluar_comandos(msg, txt):
    # print('arreglo_botones evaluar_comandos')
    # print(arreglo_botones)
    if (len(arreglo_botones)) == 0:
        bot.send_message(obtener_chat_id(msg), 'No se han podido definir los botones para ofrecerle informacion, se enviara al inicio para indicar sus datos nuevamente ')
        iniciar(msg)
        return False, txt

    txt2=txt.replace(" ","")
    txt3=txt2.lower()
    # print('txt3',txt3)
    for i in arreglo_botones:
        # print(i)
        i2=i.replace(" ","")
        i3=i2.lower()
        if (i3 == txt3):
            return True, txt3
    return False, txt


@app.route("/", methods=['GET','POST'])
def index():
    bitacora('entre index')
    try:
        if (request.method == 'POST'):
            msg  = request.get_json()
            # print(msg)
            write_json(msg, 'telegram_request.json')

            if "message" in msg and "text" in msg["message"]:
                chat_id = obtener_chat_id(msg)
                message_text = obtener_chat_text(msg)
                first_name = msg["message"]["from"]["first_name"]
                language_code = msg["message"]["from"]["language_code"]

            chat_id, txt, es_commando, es_respuesta, es_mensaje = parse_message(msg)
            print('regreso '+txt, es_commando, es_respuesta, es_mensaje)
            # if txt in BOT_COMMANDS:
            # if txt == 'algo':
            bitacora(msg)
            # logger(msg)
            if es_commando == True: #(existe_comando(txt)):
                if (txt == 'start'):
                    txt = 'iniciar'
                bot.send_message(chat_id, 'has escogido '+txt)
                # getattr(self, txt)()
                # globals()[disponibilidad]
                eval(txt)(msg)
                # print('regrese de la funcion')
            else:
                if es_respuesta:
                    procesar_respuesta(msg)
                    # bot.send_message(chat_id, 'mensaje recibido ',parse_mode='html')
                elif es_mensaje:
                    print('voy a evaluar '+txt)
                    evaluado, txt = evaluar_comandos(msg, txt)
                    if evaluado:
                        print('consegui evaluar '+txt)
                        eval(txt)(msg)
                    else:
                        bot.send_message(chat_id, 'No he entendido que quieres decir con <b><u>'+txt+'</u></b>\n No fue un comando valido. Puedes utilizar la "botonera" para ver los comandos ', parse_mode='html')
                else:
                    bot.send_message(chat_id, 'No he entendido que quieres decir con <b><u>'+txt+'</u></b>\n Puedes utilizar <b>/</b> para ver los comandos o para obtener <b>/ayuda</b> ', parse_mode='html')

            return Response('Ok', status=200)
        else:
            return "flask/bot instalado/running 5"
    except Exception as error:
        print('error en index',error)
        return "flask/bot instalado/running 5/"
        # send_message(chat_id, 'Escribiste algo que no he entendido que quieres decir con <b><u>'+txt+'</u></b>\n Puedes utilizar <b>/</b> para ver los comandos o para obtener <b>/ayuda</b> ')
        # iniciar()
    bitacora('sali index')


def ocr(msg):
    chat_id=obtener_chat_id(msg)
    imagen = Image.open('imagen.png')
    # ocr_res = pytesseract.image_to_string(imagen, lang='spa')
    ocr_res = pytesseract.image_to_string(imagen)
    print(ocr_res)

def procesar_imagen(msg):
    bitacora('entre procesar_imagen')
    try:
        chat_id=obtener_chat_id(msg)
        foto, resultado = obtener_chat_foto(msg)
        link = bot.get_file(foto['file_id'])
        downloaded_file = bot.download_file(link.file_path)
        # bitacora(downloaded_file)
        filename = str(chat_id)+'.jpg'
        with open(filename, 'wb') as new_file:
            new_file.write(downloaded_file)
        time.sleep(1)
        new_file.close()

        imagen = Image.open(filename)
        # ocr_res = pytesseract.image_to_string(imagen, lang='spa')
        ocr_res = pytesseract.image_to_string(imagen)
        print(ocr_res)
    except Exception as error:
        print('no pude procesar_imagen',chat_id,error)
    bitacora('sali procesar_imagen')


def main():
    pass

# telegramApi = TelegramApi(os.environ['TELEGRAM_API_TOKEN'])
# telegramApi = TelegramApi(TELEGRAM_API_TOKEN)
# print(telegramApi)

def logger(message):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    sys.stdout.write('{} | {}\n'.format(timestamp, message))


@app.route('/status', methods=['GET'])
def get_status():
    return 'Up and running', 201



# @app.route('/set_webhook', methods=['GET','POST'])
# def set_webhook():
#     bot.remove_webhook()
#     # s = bot.set_webhook(url="{BASE_URI}{WEBHOOK}".format(URL=BASE_URI,HOOK=TELEGRAM_API_TOKEN))
#     # s = bot.set_webhook(url="{BASE_URI}{WEBHOOK}")
#     s = bot.set_webhook(url="https://pruebaocr.cappoucla.org.ve/")
#     time.sleep(1)
#     if s:
#         return 'set_webhook Ok', 201
#     else:
#         return 'set_webhook NoOk', 201

# 
# @app.route('/',methods=['POST'])
# def webhook():
#     if request.headers.get("content-type") == "application/json":
#         update = bot.types.Update.de_json(request.stream.read().decode('utf-8'))
#         bot.process_new_update([update])
#         return "Ok",200

# @bot.message_handler(command=['start'])
# def cmd_start(message):
#     bot.send_message(message.chat.id,"Hola",parse_mode="html")

# @bot.message_handler(command=['text'])
# def bot_texto(message):
#     bot.send_message(message.chat.id,"He recibido "+message.text,parse_mode="html")


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
    # NUM_HILOS = 3

    # for num_hilo in range(NUM_HILOS):
    #     hilo = threading.Thread(name='hilo%s' %num_hilo, 
    #                             target=contar)    
    #     hilo.start()    
    print('Iniciando Bot')
    hilo = threading.Thread(name='Thread_bot',target=recibir_msg(app))
    print(hilo)
    hilo.start()
    # if (not SERVER_LOCAL):
    # print('definir_comandos ',definir_comandos())
    print('Bot iniciado')
    if not SERVER_LOCAL:
        bot.send_message(os.getenv('MI_ID_MOVISTAR', 'No definido SERVER_LOCAL'),'Reiniciado el bot '+servidor)
    # # serve(servidor, host='0.0.0.0')
    app.run(debug=True, host='0.0.0.0',port=PORT)
