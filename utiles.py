import time
import random
# , re
import os
import sys
import json

import datos as d

# from dotenv import load_dotenv
# import telebot 
# from telebot.types import ReplyKeyboardMarkup, ForceReply, ReplyKeyboardRemove


# from flask import Flask, jsonify, make_response, request, Response
# from pyngrok import ngrok, conf
# # from telegramapi import TelegramApi
# import telebot 
# import time
# import os
# import sys
# import random, re
# import json
# import requests
# # from waitress import serve
# import threading
# from telebot.types import ReplyKeyboardMarkup, ForceReply, ReplyKeyboardRemove
# # import logging
# import pytesseract
# from PIL import Image
# from dotenv import load_dotenv


def bitacora(message, file_name='registro.log'):
    # with open(file_name, 'a') as f:
        # json.dump(data, f, indent=4)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    sys.stdout.write('{} | {}\n'.format(timestamp, message))
    file=open(file_name,'a')
    file.write('{} | {}\n'.format(timestamp, message))
    file.close()

def textoAlAzar(texto):
    azar = random.randint(0,len(texto)-1)
    return texto[azar]

def saludar():
    tiempoh = time.strftime('%H',time.localtime())
    saludo = 'Buenas...'
    try:
        if tiempoh < '12':
            saludo='Buenos dias'
        elif tiempoh >= '12' and tiempoh < '18':
            saludo='Buenas tardes'
        else:
            saludo='Buenas noches'
    except Exception as error:
        print('error en saludar',error)
    bitacora('sali saludar  ')
    return saludo

def numAzar(inicio=0, fin=100):
    # utiles.bitacora('entre numAzar  ')
    azar = random.randint(inicio,fin)
    # utiles.bitacora('entre numAzar  '+str(azar))
    return azar

def obtener_chat_id(msg):
    try:
        return msg["message"]["chat"]["id"]
    except Exception as error:
        utiles.bitacora('error obtener_chat_id')

def obtener_msg_id(msg):
    try:
        return msg["message"]["reply_to_message"]["message_id"]
        # .encode('utf8')
    except Exception as error:
        utiles.bitacora('error obtener_msg_id')

def obtener_msg_id_nr(msg):
    try:
        return msg["message"]["message_id"]
    except Exception as error:
        utiles.bitacora('error obtener_msg_id_nr')

def obtener_chat_text(msg):
    try:
        return msg["message"]["text"]
        # .encode('utf8')
    except Exception as error:
        utiles.bitacora('error chat_text')

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

def evaluar_comandos(msg, txt, arreglo_botones):
    if (len(arreglo_botones)) == 0:
        bot.send_message(obtener_chat_id(msg), 'No se han podido definir los botones para ofrecerle informacion, se enviara al inicio para indicar sus datos nuevamente ')
        # iniciar(msg)
        identificarme(msg)
        return False, txt

    txt2=txt.replace(" ","")
    txt3=txt2.lower()
    # print('txt3',txt3)
    #  para los botones normales 
    for i in arreglo_botones:
        # print(i)
        i2=i.replace(" ","")
        i3=i2.lower()
        if (i3 == txt3):
            return True, txt3
    return False, txt

def colorRandom():
    number_of_colors = 31
    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        for i in range(number_of_colors)]
    return color

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
    # try:
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
        if (clave_en_lista(message['message'],'reply_to_message')):
            pregunta_hecha = d.obtener_pregunta_hecha(message)
            if (pregunta_hecha.lower() == 'mensaje a enviar') :
                txt = 'enviarMsgMasivo'
                comando = True
                # if (clave_en_lista(message['message'],'photo')):
                #     enviarMsgMasivo(message, 'photo')
                # else:
                #     enviarMsgMasivo(message, 'texto')
        else:
            comando = True
            mensaje = False
            txt = 'procesar_imagen' 
            print('recibi una imagen')

    print('sali de parse_message')
    return chat_id, txt, comando,respuesta, mensaje 
    # except Exception as error:
    #     bitacora('error parse_message')
    #     return False, False, False

def write_json(data, file_name='response.json'):
    try:
        with open(file_name, 'a') as f:
            json.dump(data, f, indent=4)
            # , ensure_ascii=False)
    except Exception as error:
        print('error en archivo json',error)
        bitacora('error en archivo json')
    bitacora('escribi en archivo json ')

