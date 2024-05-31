#!/usr/bin/env python
# coding: utf-8
'''
python3 -m venv bot-telegram
source bin/activate

pip install pytelegrambotapi
pip install requests
# pip install pyngrok
pip install flask
# pip install waitress
pip install py-mon
pip install load_dotenv
pip install pytesseract

pip install numpy
pip install matplotlib

    pymon app.py

# 
# https://api.telegram.org/bot6897485406:AAE116uTF5894G5aN0wJZ8UmfHIwRLbAnFc/getMe
# https://api.telegram.org/bot6897485406:AAE116uTF5894G5aN0wJZ8UmfHIwRLbAnFc/getUpdates
# https://api.telegram.org/bot6897485406:AAE116uTF5894G5aN0wJZ8UmfHIwRLbAnFc/deleteWebhook
# https://api.telegram.org/bot6897485406:AAE116uTF5894G5aN0wJZ8UmfHIwRLbAnFc/setWebhook?url=https://pruebaocr.cappoucla.org.ve
# https://api.telegram.org/bot6897485406:AAE116uTF5894G5aN0wJZ8UmfHIwRLbAnFc/
# https://pytba.readthedocs.io/en/latest/
# https://api.telegram.org/bot6379635079:AAHjOX9SuXHQrn-gmYQmkgBECAvG8lQ1COc/deleteWebhook
# https://api.telegram.org/bot6379635079:AAHjOX9SuXHQrn-gmYQmkgBECAvG8lQ1COc/setWebhook?url=https://pruebaspython.heros.com.ve
# https://api.telegram.org/bot6379635079:AAHjOX9SuXHQrn-gmYQmkgBECAvG8lQ1COc/setWebhook?url=https://badly-exact-skink.ngrok-free.app
# https://blog.pythonanywhere.com/148/
# 

'''




from flask import Flask, jsonify, make_response, request, Response
# from pyngrok import ngrok, conf
# from telegramapi import TelegramApi
import telebot 
from telebot.types import ReplyKeyboardMarkup, ForceReply, ReplyKeyboardRemove
import time
import os
import sys
import random
#, re
import json
import requests
# from waitress import serve
import threading
# import logging
#import pytesseract
#from PIL import Image
from dotenv import load_dotenv, find_dotenv

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import utiles as u
import datos as d
import superjefe as sj


# diractual = os.getcwd()
# load_dotenv(diractual+'.env')
load_dotenv(find_dotenv())
# load_dotenv()
URL_API         = os.getenv('URL_API', 'No definido URL_API')
u.bitacora('url api '+URL_API)
SITIOWEB        = os.getenv('SITIOWEB', 'No definido SITIOWEB')
SERVER_LOCAL    = os.getenv('SERVER_LOCAL', 'No definido SERVER_LOCAL')
SERVER_LOCAL    = True if SERVER_LOCAL=='1' else False
if (SERVER_LOCAL == True):
    TELEGRAM_API_TOKEN  = os.getenv('TELEGRAM_API_TOKEN_TEST', 'No definido TOKEN SERVER_LOCAL')
    url                 = os.getenv('SERVER_NGROK', 'No definido SERVER_LOCAL')
    servidor            = os.getenv('SERVER_NGROK', 'No definido SERVER_LOCAL')
    PORT                = os.getenv('PORT_TEST', 'No definido SERVER_LOCAL')
    print('Seleccionado SERVER_LOCAL')
    u.bitacora('Seleccionado SERVER_LOCAL '+url + servidor + str(PORT))
else:
    TELEGRAM_API_TOKEN  = os.getenv('TELEGRAM_API_TOKEN_REAL', 'No definido TOKEN SERVER_REAL')
    url                 = os.getenv('SERVER_REAL', 'No definido URL SERVER_REAL')
    servidor            = os.getenv('SERVER_REAL', 'No definido SERVER_REAL 2')
    PORT                = os.getenv('PORT_REAL', 'No definido SERVER_REAL 3')
    print('Seleccionado SERVER_REAL')
    u.bitacora('Seleccionado SERVER_REAL '+url + servidor + str(PORT)) 
RUTA_APP  = os.getenv('RUTA_APP', '/home/juanheros/demo')

bot = telebot.TeleBot(TELEGRAM_API_TOKEN)

BOT_COMMANDS= [
    {"command":"iniciar", "description":"Iniciar el Bot"},
    {"command":"identificarme","description":"Iniciar sesion de datos"},
    {"command":"ayuda", "description":"Muestra los comandos a utilizar"},
    {"command":"versiones", "description":"Muestra las actualizaciones que me han hecho"},
    {"command":"estadisticas", "description":"Muestra las estadisticas de uso"},
    {"command":"administrador", "description":"Funciones para el administrador"},
]
ADMINISTRADORES = []
AUTORIZADOS = []
# txt_pregunta_cedula = "Cuál es su número de cédula"
# txt_pregunta_codigo = "Cuál es el código de asociado"
atxt_pregunta_cedula = [
    "Cual es su numero de cedula",
    "Indiqueme su numero de cedula",
    "Escribame su numero de cedula",
    "Indiqueme por favor su numero de cedula",
    "Escribame por favor su numero de cedula"
]
atxt_pregunta_codigo = [
    "Cual es el codigo de asociado",
    "Indiqueme su codigo de asociado",
    "Escribame su el codigo de asociado",
    "Indiqueme por favor el codigo de asociado",
    "Escribame por favor el codigo de asociado"
]
txt_pregunta_cedula = 'Indiqueme por favor su numero de cedula'
txt_pregunta_codigo = 'Indiqueme por favor el codigo de asociado'
txt_si_disponibilidad = "Si, es correcto"
txt_no_disponibilidad = "No, no es correcto"
# txt_despedida = '<b>Gracias</b> por usar este servicio'
txt_despedida = [
    '<b>Gracias</b> por usar este servicio, Su sesion se ha cerrado con exito',
    'Su sesion se ha cerrado con exito, <b>Gracias</b> por usar este servicio',
    '<b>Gracias</b> Ha sido un placer ayudarte',
    'Agradezco la oportunidad de haber sido de ayuda',
    'Ha sido genial ayudarte'
    ]

datos_consulta = {
    "chat_id":0,
    "cedula":"09377388",
    "codigo":"00914",
    "id_msg_cedula":0,
    "id_msg_codigo":0,
    "saldoPrestamo" :0,
    "saldoSuspension":0
}

arreglo_botones = []
historial=[
    {
        'version'   : "1.0.0",
        'fecha'     : '2024/04/10',
        'nota'      : 'Version preliminar, pruebas de api Telegram y Endpoint bdd, pruebas de barra de progreso '
    },
    {
        'version'   : "1.1.0",
        'fecha'     : '2024/04/22',
        'nota'      : 'Realiza envio de imagenes en el saludo, validacion de sesion y botonera como menu de sesion'
    },
    {
        'version'   : "1.2.0",
        'fecha'     : '2024/04/24',
        'nota'      : 'Incorporado saludo al inicio, funcional boton prestamos'
    },
    {
        'version'   : "1.3.0",
        'fecha'     : '2024/04/25',
        'nota'      : 'Corregido no mostrar deuda pendiente, se coloco en los items saludo, disponibilidad, haberes y prestamos'
    },
    {
        'version'   : "1.3.1",
        'fecha'     : '2024/04/27',
        'nota'      : 'colocada funcion temporal /datospruebas, unificado mensaje cierre, correccion en api nombre, reimpresion de botones (desaparecen en iphone) '
    },
    {
        'version'   : "1.3.2",
        'fecha'     : '2024/05/01',
        'nota'      : 'colocada funcion para administracion'
    },
    {
        'version'   : "1.4.0",
        'fecha'     : '2024/05/09',
        'nota'      : 'algunas funciones pasadas a lista de administradores'
    },
    {
        'version'   : "1.4.1",
        'fecha'     : '2024/05/15',
        'nota'      : 'cambio de items de administradores'
    },
    {
        'version'   : "1.5.0",
        'fecha'     : '2024/05/19',
        'nota'      : 'incluida seccion de estadisticas para autorizados'
    },
    {
        'version'   : "1.6.0",
        'fecha'     : '2024/05/23',
        'nota'      : 'modularizacion'
    },
] 

nversiones = len(historial)-1
__version__ = historial[nversiones]['version']
__date__ = historial[nversiones]['fecha']
__author__ = "Juan C Hernandez B"

datos_pruebas = [
    {
        'cedula' : '7300376',
        'codigo' : '101',
        'nota'   : 'sin prestamos / deuda pendientes'
    },
    {
        'cedula' : '9377388',
        'codigo' : '914',
        'nota'   : 'con prestamos / sin deuda pendiente'
    },
    {
        'cedula' : '11787653',
        'codigo' : '357',
        'nota'   : 'sin prestamos / con deuda pendiente'
    },
    {
        'cedula' : '7349428',
        'codigo' : '622',
        'nota'   : 'con prestamos y deuda pendiente'
    }
]

este_bot = ' para Consultas de Caja de Ahorro  '
version_bot = __version__

# logger = logging.getLogger(__name__)
# logging.basicConfig(filename="logger.log",  level=logging.DEBUG)
# # encoding="utf-8",

'''
# no sacar estas funciones de este modulo
'''


def eliminar_msg(chat_id, id_msg):
    u.bitacora('entre eliminar_msg ')
    try:
        bot.delete_message(chat_id, id_msg)
    except Exception as error:
        print('no pude eliminar_msg',chat_id,id_msg,error)
    u.bitacora('sali eliminar_msg ')

def cursor_arriba(n=1):
    print(f'\33[{n}A',end='')

def barra_progreso(porcentaje, texto="", cid=None, mid=None, terminal=False):
    # u.bitacora('entre barra_progreso  '+str(porcentaje))
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
                    bot.edit_message_text('Cerrando conexion', cid, mid, parse_mode='html')
                    time.sleep(1)
                    eliminar_msg(cid, mid)
                    return
    except Exception as error:
        u.bitacora('error en barra_progreso')
        print('error en barra_progreso',error)
    # u.bitacora('sali barra_progreso  ')

def progreso(msg):
    # superjefe.progreso(msg)
    # print('regrese msg 1')
    cid = u.obtener_chat_id(msg)
    u.bitacora('entre progreso  ')
    mid = barra_progreso(0,'iniciando',cid)
    time.sleep(2)
    barra_progreso(u.numAzar(18,23),'conectando',cid, mid)
    time.sleep(2)
    barra_progreso(u.numAzar(45,55),'obteniendo datos',cid, mid)
    time.sleep(2)
    barra_progreso(u.numAzar(70,80),'procesando datos',cid, mid)
    time.sleep(2)
    barra_progreso(100,'finalizando',cid, mid)
    u.bitacora('sali progreso  ')

def solicitar_informacion(cedula, codigo, cid, mid, comando):
    u.bitacora('entre solicitar_informacion  ')
    try:
        # print('cid',cid,'mid',mid)
        barra_progreso(u.numAzar(18,25),'Obteniendo informacion API',cid, mid)
        new_data = {
            "cedula": cedula,
            "codigo": codigo,
        }
        url_post = URL_API+comando
        # print(url_post, new_data)
        # proxies = sj.dirProxy()
        # print('proxies ',proxies)
        # proxies = {
        #    'http': 'http://103.167.135.111:80',
        #    'https': 'http://116.98.229.237:10003'
        # }
        # print(proxies)

        post_response = requests.post(url=url_post, json=new_data)
        # , proxies = proxies)
        # Print the response
        post_response_json = post_response.json()
        print(post_response_json)
        u.bitacora('sali solicitar_informacion  ')
        return post_response_json
    except Exception as error:
        print('error en solicitar_informacion',error)
        u.bitacora('error en solicitar_informacion')
        return {
            "respuesta": "NoOk"
        }

def consultarDatos(msg, cid, mid, endpoint='obtenerdatosB'):
    u.bitacora('entre consultardatos')
    try:
        # cid=u.obtener_chat_id(msg)
        mid = barra_progreso(0,'Estableciendo conexion a datos',cid)
        # print('mid responder_disponibilidad',mid)
        cedula = datos_consulta['cedula']
        codigo = datos_consulta['codigo']
        respuesta = solicitar_informacion(cedula, codigo, cid, mid, endpoint)
        u.write_json(respuesta, 'telegram_request.json')
        return respuesta['respuesta'], respuesta, mid
    except Exception as error:
        print('error en consultardatos',error)
    u.bitacora('sali consultardatos  ')
    return 'NoOk', [], 0


'''
# no sacar estas funciones de este modulo
'''

def textoazar(msg):
    u.textoAlAzar(txt_despedida)

def inicializar():
    arreglo_botones = []
    datos_consulta = {
        "chat_id":0,
        "cedula":"",
        "codigo":"",
        "id_msg_cedula":0,
        "id_msg_codigo":0
    }


# def send_message(chat_id, text='nothing'):
#     sj.sendChatAction(chat_id,'text')
#     url = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage'
#     payload = {
#         'chat_id':chat_id,
#         'text':text,
#         "parse_mode":"html"
#     }
#     r = requests.post(url, json=payload)
#     u.bitacora('send_message api ')
#     return r


# def existe_comando(txt_comando):
#     existe = False
#     for comando in BOT_COMMANDS:
#         if comando['command'] == txt_comando:
#             existe = True
#             break
#     return existe

# def preguntar(chat_id, texto):
#     sj.sendchAtaction(chat_id,'text')
#     url = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/ForceReply'
#     payload = {
#         'chat_id':chat_id,
#         'text':texto,
#         "parse_mode":"html"
#     }
#     r = requests.post(url, json=payload)
#     return r

def deudapendiente(msg):
    cid=u.obtener_chat_id(msg)
    u.bitacora('entre deudapendiente ')
    sj.sendChatAction(cid,'texto')
    # mid = barra_progreso(0,'Estableciendo conexion a datos',cid)
    respuesta, resultado, mid = consultarDatos(msg, cid, 0, 'deudaPendiente')
    # print('respues en deudapendiente ',respuesta, resultado, mid)

    if respuesta =='Ok':
        respuesta=resultado
        sj.sendChatAction(cid,'texto')
        barra_progreso(u.numAzar(45,55),'Procesando informacion',cid, mid)
        time.sleep(0.5)
        sj.sendChatAction(cid,'texto')
        barra_progreso(u.numAzar(85,95),'Entregando informacion',cid, mid)
        time.sleep(0.5)
        barra_progreso(100,'Preparando la entrega de informacion',cid, mid)
        socio = respuesta['datos']
        # asocio      = float(socio['hab_f_prof'])
        # apatronal   = float(socio['hab_f_empr'])
        # reserva     = float(respuesta['reserva'])
        # asocio      = "{:,.3f}".format(asocio)
        # apatronal   = "{:,.3f}".format(apatronal)
        # reserva     = "{:,.3f}".format(reserva)
        suspensiones = respuesta['suspensiones']
        van = 0
        if len(suspensiones) > 0:
            cuento = '<b>Deuda Pendiente</b>'
            sj.sendChatAction(cid,'texto')
            bot.send_message(cid, cuento, parse_mode='html')
            time.sleep(1)
            sj.sendChatAction(cid,'texto')
            cuento = 'Los siguientes datos representan\n<b>Concepto, fallo, fecha suspension y monto</b>\n'
            try:
                for prestamo in suspensiones:
                    van = van + 1
                    saldo      = float(prestamo['monto'])
                    saldo      = "{:,.3f}".format(saldo)
                    cuento += '('+str(van)+')'
                    cuento += prestamo['prestamo'] + ' '
                    cuento += prestamo['fallo']+' '+prestamo['fsuspendido'] 
                    cuento += ' <b>'+saldo+ '</b>\n'
                bot.send_message(cid, cuento, parse_mode='html')
            except Exception as error:
                bot.send_message(cid, 'error procesando deuda pendiente', parse_mode='html')
                u.bitacora('error procesando deudapendiente')

        cuento_cierre(msg, '', respuesta['tsuspension'])

    else:
        barra_progreso(100,'Preparando entrega de informacion',cid, mid)
        markup = ReplyKeyboardRemove()
        bot.send_message(cid, '<b>No he podido obtener la informacion solicitada, revise los datos e intente de nuevo</b>', parse_mode='html')
        bot.send_message(cid, 
                '<b>Si no esta afiliado a la institucion puede visitar </b><a href="'+SITIOWEB+'">'+SITIOWEB+'</a> para su inscripcion', 
                parse_mode='html', 
                reply_markup=markup)
    u.bitacora('sali deudapendiente ')

def saldoprestamos(msg):
    cid=u.obtener_chat_id(msg)
    u.bitacora('entre saldoprestamos ')
    sj.sendChatAction(cid,'texto')
    # mid = barra_progreso(0,'Estableciendo conexion a datos',cid)
    respuesta, resultado, mid = consultarDatos(msg, cid, 0, 'obtenerPrestamos')
    # print('respues en saldohaberes ',respuesta, resultado)

    if respuesta =='Ok':
        respuesta=resultado
        sj.sendChatAction(cid,'texto')
        barra_progreso(u.numAzar(45,55),'Procesando informacion',cid, mid)
        time.sleep(0.5)
        sj.sendChatAction(cid,'texto')
        barra_progreso(u.numAzar(85,95),'Entregando informacion',cid, mid)
        time.sleep(0.5)
        barra_progreso(100,'Preparando la entrega de informacion',cid, mid)
        socio = respuesta['datos']
        asocio      = float(socio['hab_f_prof'])
        apatronal   = float(socio['hab_f_empr'])
        # reserva     = float(respuesta['reserva'])
        asocio      = "{:,.3f}".format(asocio)
        apatronal   = "{:,.3f}".format(apatronal)
        # reserva     = "{:,.3f}".format(reserva)
        afectan = respuesta['afectan']
        van = 0
        if len(afectan) > 0:
            # cuento = ''
            cuento = '<b>Saldos que <u>Afectan</u> Disponibilidad</b>\n'
            sj.sendChatAction(cid,'texto')
            # bot.send_message(cid, cuento, parse_mode='html')
            # time.sleep(1)
            # su.endChatAction(cid,'texto')
            try:
                for prestamo in afectan:
                    print(prestamo)
                    van = van + 1
                    saldo = float(prestamo['saldo'])
                    saldo = "{:,.3f}".format(saldo)
                    cuento += '('+str(van)+')'+prestamo['descr_pres']
                    cuento += ' # ' + prestamo['nropre_sdp']
                    cuento += ' ' + prestamo['descuento'] 
                    cuento += ' ('+ str(prestamo['ultcan_sdp'])+' de '+str(prestamo['nrocuotas']) + ')'
                    cuento += 'Saldo <b>'+saldo+ '</b>\n'
                bot.send_message(cid, cuento, parse_mode='html')
            except Exception as error:
                bot.send_message(cid, 'error procesando prestamos que afectan disponibilidad', parse_mode='html')
                u.bitacora('error procesando prestamos que afectan disponibilidad')

        van = 0
        afectan = respuesta['noafectan']
        if len(afectan) > 0:
            # cuento = ''
            cuento = '<b>Saldos que <u>No Afectan</u> Disponibilidad</b>\n'
            sj.sendChatAction(cid,'texto')
            # bot.send_message(cid, cuento, parse_mode='html')
            # time.sleep(1)
            # sj.sendChatAction(cid,'texto')
            try:
                for prestamo in afectan:
                    print(prestamo)
                    van = van + 1
                    saldo      = float(prestamo['saldo'])
                    saldo      = "{:,.3f}".format(saldo)
                    cuento += (str(van)+')'+prestamo['descr_pres'] + ' # '+
                    prestamo['nropre_sdp']+' '+prestamo['descuento'] + 
                    ' ('+ str(prestamo['ultcan_sdp'])+' de '+str(prestamo['nrocuotas'])+
                    ') Saldo <b>'+saldo+ '</b>\n')
                print('cuento ',cuento)
                bot.send_message(cid, cuento, parse_mode='html')
            except Exception as error:
                bot.send_message(cid, 'error procesando prestamos que NO afectan disponibilidad', parse_mode='html')
                u.bitacora('error procesando prestamos que afectan disponibilidad')

        if (len(respuesta['noafectan']) < 1) and (len(respuesta['afectan']) < 1):
            sj.sendChatAction(cid,'texto')
            bot.send_message(cid, 'No tiene prestamos registrados', parse_mode='html')

        cuento_cierre(msg, '', respuesta['tsuspension'])

    else:
        barra_progreso(100,'Preparando entrega de informacion',cid, mid)
        markup = ReplyKeyboardRemove()
        bot.send_message(cid, '<b>No he podido obtener la informacion solicitada, revise los datos e intente de nuevo</b>', parse_mode='html')
        bot.send_message(cid, 
                '<b>Si no esta afiliado a la institucion puede visitar </b><a href="'+SITIOWEB+'">'+SITIOWEB+'</a> para su inscripcion', 
                parse_mode='html', 
                reply_markup=markup)
    u.bitacora('sali saldoprestamos ')

def administrador(msg):
    chat_id=u.obtener_chat_id(msg)
    sj.sendChatAction(chat_id,'texto')
    cuento = ''
    if sj.usuarioAdministrador(chat_id):
        sj.sendChatAction(chat_id,'texto')
        arreglo_btn_admin = []
        arreglo_btn_admin.append("/datospruebas")
        arreglo_btn_admin.append("/responderbien")
        arreglo_btn_admin.append("/respondermal")
        arreglo_btn_admin.append("/progreso")
        arreglo_btn_admin.append("/estadisticas")
        arreglo_btn_admin.append("/mensajemasivo")

        # botones = ReplyKeyboardMarkup(
        #     one_time_keyboard=True, 
        #     input_field_placeholder="Puede utilizar los Botones o el menu para seleccionar", 
        #     resize_keyboard=True,
        #     row_width=3)
        for i in arreglo_btn_admin:
            # botones.add(i)
            cuento = cuento +  i + '\n' 
        # cuento = '\nOpciones disponibles '
        msg = bot.send_message(chat_id, cuento, parse_mode='html')
        # msg = bot.send_message(chat_id, cuento, reply_markup=botones, parse_mode='html')
    else: 
        msg = bot.send_message(chat_id, 'No tiene permiso para esta opcion', parse_mode='html')

def enviarGrafico(msg, datos, archivo='hoy',uso='Uso de hoy', colores=u.colorRandom()):
    chat_id=u.obtener_chat_id(msg)
    sj.sendChatAction(chat_id,'documento')
    fig, ax = plt.subplots()

    fruits = [] 
    counts = []
    bar_labels = []
    bar_colors = []

    for x, i in enumerate(datos):
        fruits.append(i['ff'])
        counts.append(i['cntChatId'])
        bar_labels.append(i['ff'][0:5])
        bar_colors.append(colores[x])
    ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

    ax.set_ylabel('Interacciones')
    ax.set_title(uso)
    plt.savefig(archivo+".jpg")

    diractual = RUTA_APP + '/'
    # foto = open('./'+archivo+'.jpg', 'rb')
    # foto = open(diractual+archivo+'.jpg', 'rb')
    sj.sendChatAction(chat_id,'foto')
    # foto = open('./images/01.jpeg', 'rb')
    foto = open(diractual+'/'+archivo+'.jpg', 'rb')
    bot.send_photo(chat_id, foto, uso)
    time.sleep(0.5)
    os.remove(archivo+".jpg")


def estadisticas(msg):
    chat_id=u.obtener_chat_id(msg)
    sj.sendChatAction(chat_id,'texto')
    cuento = ''
    try:
        if (sj.usuarioAdministrador(chat_id) or sj.usuarioAutorizado(chat_id)) :
            mid = barra_progreso(0,'Estableciendo conexion',chat_id)
            new_data = {
                "msg":"nada"
            }
            url_post = URL_API+'estadisticas'
            # print(url_post, new_data)
            u.bitacora('voy a estadisticas '+url_post)
            u.write_json(new_data, 'telegram_request.json')
            barra_progreso(u.numAzar(18,23),'Procesando datos',chat_id, mid)
            post_response = requests.post(url_post, json=new_data)
            # , proxies = sj.dirProxy())
            # Print the response
            post_response_json = post_response.json()
            # print(post_response_json)
            colores = u.colorRandom()
            barra_progreso(u.numAzar(75,95),'Entregando resultados',chat_id, mid)
            if (post_response_json['respuesta'] == 'Ok'):
                enviarGrafico(msg, post_response_json['hoy'],'hoy','Interacciones del Bot (Hoy)',colores)
                enviarGrafico(msg, post_response_json['ayer'],'ayer','Interacciones del Bot (Ayer)',colores)
                enviarGrafico(msg, post_response_json['d7'],'d7','Interacciones del Bot (Ultimos 7 dias)',colores)
                enviarGrafico(msg, post_response_json['d30'],'d30','Interacciones del Bot (Ultimos 30 dias)',colores)
            else:
                cuento = 'Lo siento... \n\n\nHubo un error para la funcion de estadisticas'
            barra_progreso(100,'terminado',chat_id, mid)

            # u.bitacora('respuesta api '+url_post)
            # u.u.write_json(post_response, 'telegram_request.json')
            u.bitacora('sali estadisticas')
            # return post_response_json
            # except Exception as error:
            #     print('error en estadisticas',error)
            #     u.bitacora('error en estadisticas')
            #     return {
            #         "respuesta": "NoOk"
            #     }
            # cuento = 'estoy en estadisticas'
        else:
            cuento = 'Lo siento... \n\n\nNo se encuentra en la lista de administradores o autorizados para esta funcion'
            bot.send_message(chat_id, cuento, parse_mode='html')
    except Exception as error:
        bot.send_message(chat_id, 'error procesando estadisticas', parse_mode='html')
        u.bitacora('error estadisticas')



def datospruebas(msg):
    chat_id=u.obtener_chat_id(msg)
    sj.sendChatAction(chat_id,'texto')
    cuento = ''
    if sj.usuarioAdministrador(chat_id):
        for version in datos_pruebas:
            cuento += version['cedula'] +' ' + version['codigo']+' =>' + version['nota']+'\n'
    else:
        cuento = 'Lo siento... \n\n\nNo se encuentra en la lista de administradores para esta funcion'
    bot.send_message(chat_id, cuento, parse_mode='html')


def versiones(msg):
    chat_id=u.obtener_chat_id(msg)
    for version in historial:
        sj.sendChatAction(chat_id,'texto')
        bot.send_message(chat_id, '<b>'+version['version'] + '</b> el '+version['fecha']+' =>' + version['nota'], parse_mode='html')
        time.sleep(0.5)

def informarpago(msg):
    chat_id=u.obtener_chat_id(msg)
    sj.sendChatAction(chat_id,'texto')
    bot.send_message(chat_id, 'Lo siento... \npendiente de desarrollo informar pago',parse_mode='html')

def cerrarsesion(msg):
    chat_id=u.obtener_chat_id(msg)
    sj.sendChatAction(chat_id,'texto')
    markup = ReplyKeyboardRemove()
    bot.send_message(chat_id, u.textoAlAzar(txt_despedida), parse_mode='html', reply_markup=markup)
    # iniciar(msg)

def botones_session(msg, nombre, saldoDeuda, enviarSaludo=False):
    # print(datos_consulta)
    if (datos_consulta['cedula'] == '' or datos_consulta['codigo']==''):
        bot.send_message(chat_id, 'Lo siento... \nAlgo malo ha ocurrido con los datos para obtener sesion, <b>revise sus datos e intente nuevamente</b>',parse_mode='html')
        # iniciar()
        identificarme(msg)

    chat_id=u.obtener_chat_id(msg)
    sj.sendChatAction(chat_id,'texto')

    # validar que tenga informacion de cedula y codigo 
    # la funcion disponibilidad cambiarla para no pedir los datos

    txt_Disponibilidad  = 'Disponibilidad'
    txt_haberes         = 'Saldo Haberes'
    txt_prestamos       = 'Saldo Prestamos'
    txt_pendiente       = 'Deuda Pendiente'
    txt_pagos           = 'Informar Pago'
    txt_salir           = 'Cerrar Sesion'

    # print('arreglo_botones antes')
    # print(arreglo_botones)
    if len(arreglo_botones) < 1:
        arreglo_botones.append(txt_Disponibilidad)
        arreglo_botones.append(txt_haberes)
        arreglo_botones.append(txt_prestamos)
        arreglo_botones.append(txt_pendiente)
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
    if datos_consulta['saldoPrestamo'] > 0:
        if datos_consulta['saldoSuspension'] > 0:
            botones.row(txt_haberes, txt_prestamos, txt_pendiente)
        else:
            botones.row(txt_haberes, txt_prestamos)
    else:
        if datos_consulta['saldoSuspension'] > 0:
            botones.row(txt_haberes, txt_pendiente)
        else:
            botones.row(txt_haberes)
    botones.row(txt_pagos)
    botones.row(txt_salir)
    cuento = ''
    if enviarSaludo:
        cuento = u.saludar()+' <b>'+nombre.strip()+'</b>\n'
        cuento += saldoPendiente(saldoDeuda)
    cuento += '\nOpciones disponibles '
    msg = bot.send_message(chat_id, cuento, reply_markup=botones, parse_mode='html')
    # definir_comandos(BOT_COMMANDS)


def botones_inicio(msg):
    chat_id=u.obtener_chat_id(msg)
    sj.sendChatAction(chat_id,'texto')
    sj.definir_comandos(BOT_COMMANDS)

# def menu_anterior(msg):
#     botones_inicio(BOT_COMMANDS)

def ayuda(msg):
    inicializar()
    chat_id=u.obtener_chat_id(msg)
    # print('estoy en ayuda')
    sj.sendChatAction(chat_id,'texto')
    texto =  "<b>Commandos que pueden utilizarse</b>\n" \
            "/iniciar - <b>Inicia el servicio de bot</b>\n" \
            "/identificarme - <b>Iniciar sesion de datos</b>\n" \
            "/ayuda - <b>Este mensaje</b>"
            # "/disponibilidad - <b>Obtener su disponibilidad</b>\n" \
    markup = ReplyKeyboardRemove()
    bot.send_message(chat_id, texto, parse_mode="html",reply_markup=markup)
    botones_inicio(msg)
    u.bitacora('funcion ayuda ')


def iniciar(msg):
    # print('estoy en iniciar')
    u.bitacora('funcion iniciar ')
    inicializar()
    chat_id=u.obtener_chat_id(msg)
    sj.sendChatAction(chat_id,'texto')
    markup = ReplyKeyboardRemove()
    cuento = "<b><i>Bienvenido(a) al Bot "+este_bot + version_bot + '</i></b>\n\n'
    cuento += 'Utilizando tecla <b>/</b> puede obtener los comandos disponibles o bien si le aparece el menú también puede utilizarlo\n'
    cuento += '\nSi desea obtener la disponibilidad debe seguir los pasos indicados, le envio la imagen de referencia'
    bot.send_message(chat_id, cuento, parse_mode="html", reply_markup=markup)
    botones_inicio(msg)

    diractual = RUTA_APP + '/images/'
    sj.sendChatAction(chat_id,'foto')
    # foto = open('./images/01.jpeg', 'rb')
    foto = open(diractual+'01.jpeg', 'rb')
    bot.send_photo(chat_id, foto, 'Ejemplo para obtener su disponibilidad')

    sj.sendChatAction(chat_id,'foto')
    # foto = open('./images/02.jpeg', 'rb')
    foto = open(diractual+'02.jpeg', 'rb')
    bot.send_photo(chat_id, foto)

    sj.sendChatAction(chat_id,'foto')
    # foto = open('./images/03.jpeg', 'rb')
    foto = open(diractual+'03.jpeg', 'rb')
    bot.send_photo(chat_id, foto)
    sj.sendChatAction(chat_id,'foto')

    foto = open(diractual+'04.jpeg', 'rb')
    # foto = open('./images/04.jpeg', 'rb')
    bot.send_photo(chat_id, foto)
    foto = open(diractual+'04.jpeg', 'rb')
    u.bitacora('fin funcion iniciar ')


def confirmar_datos(message):
    u.bitacora('entre confirmar_datos ')
    try:
        print('estoy en confirmar_datos')
        # print(message)
        print(datos_consulta)
        chat_id = u.obtener_chat_id(message)
        texto = u.obtener_chat_text(message)
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
                respuesta, resultado, mid = consultarDatos(message, chat_id, 0)
                print('respues en confirmar_datos ',respuesta, resultado)
                if respuesta == 'Ok':
                    eliminar_msg(chat_id, mid)
                    # print('prestamos ',float(resultado['afectan']['saldo'])+float(resultado['noafectan']['saldo']))
                    # print('pediente ',float(resultado['tsuspension']))
                    datos_consulta['saldoPrestamo']=float(resultado['afectan']['saldo'])+float(resultado['noafectan']['saldo'])
                    datos_consulta['saldoSuspension']=float(resultado['tsuspension'])
                    cuento = resultado['datos']['ape_prof'].strip() + ' ' + resultado['datos']['nombr_prof'].strip()+'\n'
                    # cuento += saldoPendiente(resultado['tsuspension'])
                    botones_session(message, cuento, resultado['tsuspension'], True)
                else:
                    markup = ReplyKeyboardRemove()
                    bot.send_message(chat_id, 
                        'Lo sentimos, tuvimos inconveniente para iniciar sesion',
                        parse_mode='html',
                        reply_markup=markup)
                    identificarme(message)
                    if (mid != 0):
                        eliminar_msg(chat_id, mid)
    except Exception as error:
        print('error en confirmar_datos',error)
        bot.send_message(chat_id, 'Lo siento... \nAlgo malo ha ocurrido con los datos, <b>revise sus datos e intente nuevamente</b>',parse_mode='html')
    u.bitacora('sali confirmar_datos ')

def preguntar_codigo(message):
    u.bitacora('entre preguntar_codigo ')
    # print(message)
    chat_id = u.obtener_chat_id(message)
    texto = u.obtener_chat_text(message)
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
    u.bitacora('sali preguntar_codigo ')

def cuento_cierre(msg, nombre, saldoDeuda):
    cid = u.obtener_chat_id(msg)
    cuento = ''
    cuento += '\nPara mayor informacion puede consultar el Estado de Cuenta en '
    cuento += '<a href="https://estadodecuenta.cappoucla.org.ve">Estado de Cuenta</a>\n'
    cuento += '\nIgualmente lo invitamos a visitar regularmente nuestro sitio web '
    # cuento += '<a href="https://cappoucla.org.ve">cappoucla.org.ve</a>\n'
    cuento += '<a href="'+SITIOWEB+'">'+SITIOWEB+'</a>\n'
    sj.sendChatAction(cid,'texto')
    bot.send_message(cid, cuento, parse_mode='html')
    botones_session(msg, nombre, saldoDeuda, False)


def saldohaberes(msg):
    cid=u.obtener_chat_id(msg)
    u.bitacora('entre saldohaberes ')
    sj.sendChatAction(cid,'texto')
    # mid = barra_progreso(0,'Estableciendo conexion a datos',cid)
    try:
        respuesta, resultado, mid = consultarDatos(msg, cid, 0)
        # print('respues en saldohaberes ',respuesta, resultado)

        if respuesta =='Ok':
            respuesta=resultado
            sj.sendChatAction(cid,'texto')
            barra_progreso(u.numAzar(45,55),'Procesando informacion',cid, mid)
            time.sleep(0.5)
            sj.sendChatAction(cid,'texto')
            barra_progreso(u.numAzar(85,95),'Entregando informacion',cid, mid)
            time.sleep(0.5)
            barra_progreso(100,'Preparando la entrega de informacion',cid, mid)
            socio = respuesta['datos']
            # cuento = "Estimado(a) Socio(a):<b><span class='tg-spoiler'>"+socio['nombre']+'</span><b>\n'
            asocio      = float(socio['hab_f_prof'])
            apatronal   = float(socio['hab_f_empr'])
            reserva     = float(respuesta['reserva'])
            asocio      = "{:,.3f}".format(asocio)
            apatronal   = "{:,.3f}".format(apatronal)
            reserva     = "{:,.3f}".format(reserva)
            cuento = "Estimado(a) Socio(a):<b>"+socio['nombre']+'</b>\n'
            cuento += 'Datos actualizados el <b>'+respuesta['actualizacion']['fechaactdatos']+'</b>\n'
            cuento += 'Ahorros Socio al '+socio['uas']+': <b>'+asocio+'</b>\n'
            cuento += 'Aporte Patronal al '+socio['uap']+': <b>'+apatronal+'</b>\n'
            cuento += '<u>Menos</u> Reserva Legal <b>'+reserva+'</b>\n'

            cuento += saldoPendiente(respuesta['tsuspension'])

            # cuento += '\nPara mayor informacion puede consultar el Estado de Cuenta en '
            # cuento += '<a href="https://estadodecuenta.cappoucla.org.ve">Estado de Cuenta</a>\n'
            # cuento += '\nIgualmente lo invitamos a visitar regularmente nuestro sitio web '
            # cuento += '<a href="'+SITIOWEB+'">'+SITIOWEB+'</a>\n'
            sj.sendChatAction(cid,'texto')
            bot.send_message(cid, cuento, parse_mode='html')
            cuento_cierre(msg, '', respuesta['tsuspension'])
        else:
            barra_progreso(100,'Preparando entrega de informacion',cid, mid)
            markup = ReplyKeyboardRemove()
            bot.send_message(cid, '<b>No he podido obtener la informacion solicitada, revise los datos e intente de nuevo</b>', parse_mode='html')
            bot.send_message(cid, 
                    '<b>Si no esta afiliado a la institucion puede visitar </b><a href="'+SITIOWEB+'">'+SITIOWEB+'</a> para su inscripcion', 
                    parse_mode='html', 
                    reply_markup=markup)
        u.bitacora('sali disponibilidad ')
    except Exception as error:
        u.bitacora('error saldohaberes')

def disponibilidad(msg):
    chat_id=u.obtener_chat_id(msg)
    u.bitacora('entre disponibilidad ')
    sj.sendChatAction(chat_id,'texto')
    responder_disponibilidad(msg)
    u.bitacora('sali disponibilidad ')
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


def saldoPendiente(saldo=0):
    if (float(saldo) > 0):
        tsuspension     = float(saldo)
        tsuspension     = "{:,.3f}".format(tsuspension)
        return '\n<b>Tiene un saldo pendiente de '+tsuspension+'</b>\n\n'
    else:
        return '\n'


def responder_disponibilidad(msg):
    cid = u.obtener_chat_id(msg)
    u.bitacora('entre responder_disponibilidad  ')
    try:
        mid = barra_progreso(0,'Estableciendo conexion a datos',cid)
        # print('mid responder_disponibilidad',mid)
        cedula = datos_consulta['cedula']
        codigo = datos_consulta['codigo']
        respuesta = solicitar_informacion(cedula, codigo, cid, mid, 'obtenerdatosB')
        u.write_json(respuesta, 'telegram_request.json')
        print(respuesta)
        # u.write_json(respuesta, 'telegram_request.json')
        if respuesta['respuesta'] =='Ok':
            sj.sendChatAction(cid,'texto')
            barra_progreso(u.numAzar(45,55),'Procesando informacion',cid, mid)
            time.sleep(0.5)
            sj.sendChatAction(cid,'texto')
            barra_progreso(u.numAzar(85,95),'Entregando informacion',cid, mid)
            time.sleep(0.5)
            barra_progreso(100,'Preparando entrega de informacion',cid, mid)
            socio = respuesta['datos']
            disponibilidad     = float(respuesta['disponibilidad'])
            disponibilidad     = "{:,.3f}".format(disponibilidad)


            # cuento = "Estimado(a) Socio(a):<b><span class='tg-spoiler'>"+socio['nombre']+'</span><b>\n'
            cuento = "Estimado(a) Socio(a): <b>"+socio['nombre']+'</b>\n'
            cuento += 'Su disponibilidad es de <b>'+disponibilidad+'</b>\n'
            cuento += saldoPendiente(respuesta['tsuspension'])
            cuento += 'Datos actualizados el '+respuesta['actualizacion']['fechaactdatos']+'\n'
            # cuento += '\nPara mayor informacion puede consultar el Estado de Cuenta en '
            # cuento += '<a href="https://estadodecuenta.cappoucla.org.ve">Estado de Cuenta</a>\n'
            # cuento += '\nIgualmente lo invitamos a visitar regularmente nuestro sitio web '
            # # cuento += '<a href="https://cappoucla.org.ve">cappoucla.org.ve</a>\n'
            # cuento += '<a href="'+SITIOWEB+'">'+SITIOWEB+'</a>\n'
            sj.sendChatAction(cid,'texto')
            bot.send_message(cid, cuento, parse_mode='html')
            cuento_cierre(msg, '', respuesta['tsuspension'])

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
    u.bitacora('sali responder_disponibilidad  ')

def responderbien(msg):
    cid=u.obtener_chat_id(msg)
    if sj.usuarioAdministrador(cid):
        datos_consulta['cedula']='09377388'
        datos_consulta['codigo']='00914'
        responder_disponibilidad(msg)
    else:
        cuento = 'Lo siento... \n\n\nNo se encuentra en la lista de administradores para esta funcion'
        bot.send_message(chat_id, cuento, parse_mode='html')


def respondermal(msg):
    cid=u.obtener_chat_id(msg)
    if sj.usuarioAdministrador(cid):
        datos_consulta['cedula']='0937738'
        datos_consulta['codigo']='00914'
        responder_disponibilidad(msg)
    else:
        cuento = 'Lo siento... \n\n\nNo se encuentra en la lista de administradores para esta funcion'
        bot.send_message(chat_id, cuento, parse_mode='html')

def identificarme(msg):
    chat_id=u.obtener_chat_id(msg)
    u.bitacora('entre identificarme ')
    sj.sendChatAction(chat_id,'texto')
    botones = ReplyKeyboardRemove()
    # global txt_pregunta_cedula = textoAlAzar(txt_pregunta_cedula)
    # global txt_pregunta_codigo = textoAlAzar(txt_pregunta_codigo)
    # respuesta = bot.send_message(chat_id, '',reply_markup=botones)
    markup = ForceReply()
    respuesta = bot.send_message(
        chat_id, 
        txt_pregunta_cedula,reply_markup = markup, 
        parse_mode='html')
    # print(respuesta)
    bot.register_next_step_handler(respuesta, preguntar_codigo)
    u.bitacora('sali identificarme ')


def procesar_respuesta(msg):
    u.bitacora('entre procesar_respuesta  ')
    try:
        pregunta_hecha = d.obtener_pregunta_hecha(msg)
        chat_id = u.obtener_chat_id(msg)
        print('la pregunta hecha',pregunta_hecha, txt_pregunta_cedula.lower())
        if pregunta_hecha.lower() == txt_pregunta_cedula.lower():
            texto = u.obtener_chat_text(msg)
            if not texto.isdigit(): # preguntar codigo
                disponibilidad(msg)
            else:
                texto = texto.zfill(8)
                datos_consulta['cedula']=texto
                datos_consulta['id_msg_cedula']=u.obtener_msg_id(msg)
                print('entre cedula es digito ')
                preguntar_codigo(msg)
        if pregunta_hecha.lower() == txt_pregunta_codigo.lower():
            texto = u.obtener_chat_text(msg)
            if not texto.isdigit(): # preguntar codigo
                preguntar_codigo(msg)
            else:
                texto = texto.zfill(5)
                datos_consulta['codigo']=texto
                datos_consulta['id_msg_codigo']=u.obtener_msg_id(msg)
                confirmar_datos(msg)
        if pregunta_hecha.lower() == 'mensaje a enviar':
            enviarMsgMasivo(msg)
        u.bitacora('sali procesar_respuesta  ')
        # if pregunta_hecha.lower() == txt_si_disponibilidad.lower():
        #     responder_disponibilidad(msg)
    except Exception as error:
        print('error en procesar_respuesta',error)
        u.bitacora('error en procesar_respuesta')
        bot.send_message(chat_id, 'Escribiste algo que no he entendido que quieres decir con <b><u>'+txt+'</u></b>\n Puedes utilizar <b>/</b> para ver los comandos o para obtener <b>/ayuda</b> ',parse_mode='html')
        iniciar()


    # bot.send_message(u.obtener_chat_id(msg),'estoy en procesar_respuesta')


# def delete_webhook():
#     u.bitacora('deleteWebhook')
#     listo = False
#     try:
#         if bot.delete_webhook():
#             u.bitacora('eliminado webhook')
#             listo = True
#         else:
#             u.bitacora("error en delete_webhook")
#     except Exception as error:
#         u.bitacora("error delete_webhook")
#     return listo

# def set_webhook(dir_url, TELEGRAM_API_TOKEN):
#     u.bitacora('set_webhook')
#     listo = False
#     try:
#         if bot.set_webhook(url=dir_url, max_connections=20):
#             u.bitacora('asignado set_webhook')
#             listo = True
#         else:
#             u.bitacora("error  en set_webhook")
#     except Exception as error:
#         u.bitacora("error set_webhook")
#         print(error)
#     return listo


def recibir_msg(app):
    listo = False
    u.bitacora('entre recibir_msg')
    try:
        # res = sj.deleteWebhook(TELEGRAM_API_TOKEN)
        if sj.delete_webhook(bot):
            # if res['ok']:
            time.sleep(1)
            if sj.set_webhook(bot, url, TELEGRAM_API_TOKEN):
                # if res['ok']:
                id = os.getenv('MI_ID_MOVISTAR', 'No definido SERVER_LOCAL')
                bot.send_message(id,'asignado Webhook '+servidor)
                listo = True
            else:
                u.bitacora("error  en set_webhook")
        else:
            u.bitacora("error en delete_webhook")

            #     return True
            # except Exception as error:
            #     print('fallo inicio configuracion bot ',error)
            #     return False
            u.bitacora('sali recibir_msg')
    except Exception as error:
        u.bitacora('error recibir_msg')
    return listo


def print_properties(value, parent):
    if type(value) is dict:
        for (key, val) in value.items():
            if type(val) is dict:
                print_properties(val, parent + '.' + key)
            else:
                print("{}: {}".format(parent + '.' + key, val))
                u.bitacora("{}: {}".format(parent + '.' + key, val))
    else:
        u.bitacora("{}: {}".format(parent, value))

def ocr(msg):
    chat_id=u.obtener_chat_id(msg)
    imagen = Image.open('imagen.png')
    # ocr_res = pytesseract.image_to_string(imagen, lang='spa')
    ocr_res = pytesseract.image_to_string(imagen)
    print(ocr_res)

def procesar_imagen(msg):
    u.bitacora('entre procesar_imagen')
    try:
        chat_id=u.obtener_chat_id(msg)
        foto, resultado = u.obtener_chat_foto(msg)
        link = bot.get_file(foto['file_id'])
        downloaded_file = bot.download_file(link.file_path)
        # u.bitacora(downloaded_file)
        filename = str(chat_id)+'.jpg'
        with open(filename, 'wb') as new_file:
            new_file.write(downloaded_file)
        time.sleep(1)
        new_file.close()

        imagen = Image.open(filename)
        # ocr_res = pytesseract.image_to_string(imagen, lang='spa')
        ocr_res = pytesseract.image_to_string(imagen)
        print(ocr_res)
        bot.send_message(u.obtener_chat_id(msg), 'lo que pude extraer de la imagen recibida')
        if (len(ocr_res.strip()) > 0):
            bot.send_message(u.obtener_chat_id(msg), ocr_res)
        else:
            bot.send_message(u.obtener_chat_id(msg), 'no pude obtener informacion de la imagen recibida')
    except Exception as error:
        print('no pude procesar_imagen',chat_id,error)
    u.bitacora('sali procesar_imagen')

def enviarMsgMasivo(msg):
    chat_id=u.obtener_chat_id(msg)
    if sj.usuarioAdministrador(chat_id):
        sj.sendChatAction(chat_id,'texto')
        respuesta = bot.send_message(
            chat_id, 
            msg,
            parse_mode='html')


def mensajemasivo(msg):
    u.bitacora('entre mensajeUsuarios')
    try:
        chat_id=u.obtener_chat_id(msg)
        if sj.usuarioAdministrador(chat_id):
            bot.send_message(chat_id, 'es un administrador')
            sj.sendChatAction(chat_id,'texto')
            botones = ReplyKeyboardRemove()
            # global txt_pregunta_cedula = textoAlAzar(txt_pregunta_cedula)
            # global txt_pregunta_codigo = textoAlAzar(txt_pregunta_codigo)
            # respuesta = bot.send_message(chat_id, '',reply_markup=botones)
            markup = ForceReply()
            respuesta = bot.send_message(
                chat_id, 
                'Mensaje a enviar',reply_markup = markup, 
                parse_mode='html')
            print(respuesta)
            bot.register_next_step_handler(respuesta, enviarMsgMasivo)
        else:
            bot.send_message(chat_id, 'no es un administrador')
    except Exception as error:
        print('no pude mensajeUsuarios',chat_id,error)
    u.bitacora('sali mensajeUsuarios')

# def reiniciar(msg):
#     try:
#         chat_id=u.obtener_chat_id(msg)
#         if sj.usuarioAdministrador(chat_id):
#             bot.delete_message(chat_id, u.obtener_msg_id_nr(msg))
#             bot.send_message(chat_id, 'intento reiniciar servicio')
#             u.bitacora('reiniciando servicio en 3 segundos')
#             time.sleep(3)
#             sys.stdout.flush()
#             # os.execv(sys.argv[0], sys.argv)
#             os.execv(sys.executable, [sys.executable] + sys.argv)
#             u.bitacora('reiniciando servicio')
#         else:
#             bot.send_message(chat_id, 'no es un usuario administrador')
#     except Exception as error:
#         print('no pude reiniciar',chat_id, error)
#     u.bitacora('sali reiniciar')

def main():
    pass

# telegramApi = TelegramApi(os.environ['TELEGRAM_API_TOKEN'])
# telegramApi = TelegramApi(TELEGRAM_API_TOKEN)
# print(telegramApi)

def logger(message):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    sys.stdout.write('{} | {}\n'.format(timestamp, message))


app = Flask(__name__)
@app.route("/", methods=['GET','POST'])
def index():
    u.bitacora('entre index')
    try:
        if (request.method == 'POST'):
            msg  = request.get_json(force=True,silent=True)

            a = json.dumps(msg)
            u.bitacora('enviar a registrar_peticion')
            # b = json.loads(a)
            sj.registrar_peticion(msg)
            u.bitacora('regreso de registrar_peticion y registrare json msg')
            # for (key, val) in msg.items():
            #     print_properties(val, key)

            # silent=True
            # params = json.dumps(msg).encode('utf8')
            # u.bitacora(msg)
            u.write_json(msg, 'telegram_request.json')
            u.bitacora('regreso registrar json msg')

            if "message" in msg and "text" in msg["message"]:
                chat_id = u.obtener_chat_id(msg)
                message_text = u.obtener_chat_text(msg)
                first_name = msg["message"]["from"]["first_name"]
                language_code = msg["message"]["from"]["language_code"]

            chat_id, txt, es_commando, es_respuesta, es_mensaje = u.parse_message(msg)
            print('regreso '+txt, es_commando, es_respuesta, es_mensaje)
            cuento = 'respuesta de parse_message => '+txt
            # u.bitacora('respuesta de parse_message => '+txt)
            if es_commando:
                cuento += ' es un comando'
                # u.bitacora('es un comando ')
            elif es_respuesta:
                cuento += ' es una respuesta'
                # u.bitacora('es una respuesta ')
            else:
                cuento += ' es un mensaje'
                # u.bitacora('es un mensaje ')
            u.bitacora(cuento)
            # if txt in BOT_COMMANDS:
            # if txt == 'algo':
            # u.bitacora(msg)
            # logger(msg)
            if es_commando: #(existe_comando(txt)):
                if (txt == 'start'):
                    txt = 'iniciar'
                u.bitacora('i1')
                bot.send_message(chat_id, 'Seleccionaste <i>'+txt+'</i>', parse_mode='html')
                u.bitacora('i2')
                # getattr(self, txt)()
                # globals()[disponibilidad]
                try:
                    eval(txt)(msg)
                except Exception as error:
                    bot.send_message(chat_id, '1. No he entendido que quieres decir con <b><u>'+txt+'</u></b>\n No fue un comando valido. Puedes utilizar la "botonera" para ver los comandos ', parse_mode='html')
                    print(error)
                # print('regrese de la funcion')
            else:
                if es_respuesta:
                    procesar_respuesta(msg)
                    # bot.send_message(chat_id, 'mensaje recibido ',parse_mode='html')
                elif es_mensaje:
                    print('voy a evaluar ==> '+txt)
                    # print(arreglo_botones)
                    evaluado, txt = u.evaluar_comandos(msg, txt, arreglo_botones)
                    if evaluado:
                        print('consegui evaluar '+txt)
                        try:
                            eval(txt)(msg)
                        except Exception as error:
                            bot.send_message(chat_id, '2. No he entendido que quieres decir con <b><u>'+txt+'</u></b>\n No fue un comando valido. Puedes utilizar la "botonera" para ver los comandos ', parse_mode='html')
                    else:
                        bot.send_message(chat_id, '3. No he entendido que quieres decir con <b><u>'+txt+'</u></b>\n No fue un comando valido. Puedes utilizar la "botonera" para ver los comandos ', parse_mode='html')
                else:
                    bot.send_message(chat_id, '4. No he entendido que quieres decir con <b><u>'+txt+'</u></b>\n Puedes utilizar <b>/</b> para ver los comandos o para obtener <b>/ayuda</b> ', parse_mode='html')

            return Response('Ok', status=200)
        else:
            u.bitacora("URL API "+URL_API)
            return "flask/bot instalado/running 5"
    except Exception as error:
        # bot.send_message(os.getenv('MI_ID_MOVISTAR', 'No definido SERVER_LOCAL'), 'reiniciar bot'+error, parse_mode='html')
        print('error en index',error)
        return "excepcion flask/bot instalado/running 5/"
        # send_message(chat_id, 'Escribiste algo que no he entendido que quieres decir con <b><u>'+txt+'</u></b>\n Puedes utilizar <b>/</b> para ver los comandos o para obtener <b>/ayuda</b> ')
        # iniciar()
    u.bitacora('sali index')


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
    # cargar_administradores()
    '''
    # NUM_HILOS = 3

    # for num_hilo in range(U.Num_HILOS):
    #     hilo = threading.Thread(name='hilo%s' %num_hilo, 
    #                             target=contar)    
    #     hilo.start()    
    '''
    # print('Iniciando Bot')
    '''
    # hilo = threading.Thread(name='Thread_bot',target=recibir_msg(app))
    # print(hilo)
    # hilo.start()
    # if (not SERVER_LOCAL):
    # print('definir_comandos ',definir_comandos())
    # print('Bot iniciado')
    # if not SERVER_LOCAL:
    # # serve(servidor, host='0.0.0.0')
    # txt_pregunta_cedula = textoAlAzar(atxt_pregunta_cedula)
    # txt_pregunta_codigo = textoAlAzar(atxt_pregunta_codigo)
    '''
    # print('las preguntas a usar ',txt_pregunta_cedula, txt_pregunta_codigo)
    u.bitacora('iniciando bot, mensaje a '+TELEGRAM_API_TOKEN)
    # if recibir_msg(app):
    id = os.getenv('MI_ID_MOVISTAR', 'No definido SERVER_LOCAL')
    bot.send_message(id,'Reiniciado el bot '+servidor + ' '+este_bot + 'Version ' + version_bot)
    # print(sj.dirProxy())
    app.run(debug=True, host='0.0.0.0',port=PORT)
    # else:
    #     u.bitacora('error iniciando servicio')


'''
    comandos
    /iniciar
    /identificarme
    /ayuda
    /versiones
    /administrador

    /datospruebas
    /responderbien
    /respondermal
    /progreso
    /estadisticas
    /mensajemasivo

'''