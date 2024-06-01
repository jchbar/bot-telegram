import time
import random, re
import os
import sys
from dotenv import load_dotenv, find_dotenv
# from flask import Flask, jsonify, make_response, request, Response
import requests
import json
# from fp.fp import FreeProxy

# https://pypi.org/project/free-proxy/


import utiles as u

def cargarEntorno():
    load_dotenv(find_dotenv())
    URL_API         = os.getenv('URL_API', 'No definido URL_API')
    SERVER_LOCAL    = os.getenv("SERVER_LOCAL", "No definido SERVER_LOCAL")
    SERVER_LOCAL    = True if SERVER_LOCAL=="1" else False
    if (SERVER_LOCAL == True):
        TELEGRAM_API_TOKEN  = os.getenv("TELEGRAM_API_TOKEN_TEST", "No definido TOKEN SERVER_LOCAL")
        url                 = os.getenv("SERVER_NGROK", "No definido SERVER_LOCAL")
    else:
        TELEGRAM_API_TOKEN  = os.getenv("TELEGRAM_API_TOKEN_REAL", "No definido TOKEN SERVER_REAL")
        url                 = os.getenv("SERVER_REAL", "No definido URL SERVER_REAL")
    # print("cargue superjefe", TELEGRAM_API_TOKEN)
    return TELEGRAM_API_TOKEN, url, URL_API

def deleteWebhook(TELEGRAM_API_TOKEN):
    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/deleteWebhook"
    payload = {
        # "chat_id":chat_id,
        # "action":mostrar
    }
    try:
        r = requests.post(url, json=payload)
        u.bitacora(r)
    except Exception as error:
        u.bitacora("deleteWebhook api")
        print("error en deleteWebhook",error)
    u.bitacora("escribi en archivo json ")
    return r

def setWebhook(url, TELEGRAM_API_TOKEN):
    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/setWebhook?url="+url
    payload = {
        # "url":url,
        # "action":mostrar
    }
    try:
        r = requests.post(url) #, json=payload)
        print ("setWebhook",url)
        u.bitacora("setWebhook api "+url)
    except Exception as error:
        u.bitacora("setWebhook api "+url)
        print("error en setWebhook",error)
    u.bitacora(r)
    return r

def delete_webhook(bot):
    u.bitacora('deleteWebhook')
    listo = False
    try:
        if bot.delete_webhook():
            u.bitacora('eliminado webhook')
            listo = True
        else:
            u.bitacora("error en delete_webhook")
    except Exception as error:
        u.bitacora("error delete_webhook")
    return listo

def set_webhook(bot, dir_url, TELEGRAM_API_TOKEN):
    u.bitacora('set_webhook')
    listo = False
    try:
        if bot.set_webhook(url=dir_url, max_connections=20):
            u.bitacora('asignado set_webhook')
            listo = True
        else:
            u.bitacora("error  en set_webhook")
    except Exception as error:
        u.bitacora("error set_webhook")
        print(error)
    return listo



# def eliminarw():
#     deleteWebhook()

# def asignarw():
#     setWebhook(url):

def sendChatAction(chat_id, tipo:"texto"):
    u.bitacora('sendChatAction chat_id'+str(chat_id)+' tipo '+tipo)
    TELEGRAM_API_TOKEN, url, URL_API = cargarEntorno()
    # print("token ")
    # print("TELEGRAM_API_TOKEN", TELEGRAM_API_TOKEN, "url ",url)
    # funcion en python 3.10
    # match tipo:
    #     case  "texto":
    #         mostrar="typing"
    #     case "foto"  :   
    #         mostrar="upload_photo"
    #     case "video" :   
    #         mostrar="upload_video"
    #     case "voz"   :   
    #         mostrar="upload_voice"
    #     case "documento":
    #         mostrar="upload_document"
    #     case "sticker":  
    #         mostrar="choose_sticker"
    #     case "ubicacion" : 
    #         mostrar="find_location"
    if tipo == "texto":
        mostrar="typing"
    elif tipo == "foto":   
        mostrar="upload_photo"
    elif tipo == "video":   
        mostrar="upload_video"
    elif tipo ==  "voz":   
        mostrar="upload_voice"
    elif tipo == "documento":
        mostrar="upload_document"
    elif tipo == "sticker":  
        mostrar="choose_sticker"
    elif tipo ==  "ubicacion" : 
        mostrar="find_location"
    else:
        mostrar = "typing"
    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendChatAction"
    payload = {
        "chat_id":chat_id,
    "action":mostrar
    }
    r = requests.post(url, json=payload)
    u.bitacora('termine sendChatAction')
    return r

# https://stackoverflow.com/questions/73845184/implementing-commands-menu-button-for-a-telegram-bot-using-telebot
def definir_comandos(BOT_COMMANDS):
    u.bitacora('dc1')
    TELEGRAM_API_TOKEN, url, URL_API = cargarEntorno()
    # BOT_COMMANDS= [{"command":"Iniciar", "description":"Iniciar el Bot"},{"command":"Disponibilidad","description":"Obtener mi Disponibilidad"}]
    u.bitacora('dc2')
    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/setMyCommands"
    u.bitacora('dc3')
    # payload = {
    #     "chat_id":chat_id,
    #     "action":mostrar
    # }
    # r = requests.post(url, json=payload)
    u.bitacora('dc4')
    u.bitacora("definir_comandos url "+url)
    u.bitacora('dc5')
    send_text = url + "?commands=" + str(json.dumps(BOT_COMMANDS) ) 
    u.bitacora("entre definir_comandos "+send_text)
    try:
        u.bitacora(send_text)
        r  = requests.get(send_text, verify=False)
        u.bitacora("sali definir_comandos")
    except Exception as error:
        u.bitacora("error definir_comandos")
    return r

def registrar_peticion(msg):
    u.bitacora("entre registrar_peticion")
    TELEGRAM_API_TOKEN, url, URL_API = cargarEntorno()
    try:
        # print("cid",cid,"mid",mid)
        new_data = {
            "message": msg
        }
        url_post = URL_API+"guardarSolicitudTG"
        # u.bitacora('url_post' + url_post)
        # print(url_post, new_data)
        u.bitacora("voy a api "+url_post+' escribire solicitud')
        u.write_json(new_data, "telegram_request.json")
        post_response = requests.post(url_post, json=new_data)
        # u.bitacora(post_response)
        # Print the response
        post_response_json = post_response.json()
        u.bitacora("respuesta api "+url_post+' escribire respuesta')
        u.write_json(post_response_json, "telegram_request.json")
        u.bitacora("sali registrar_peticion")
        return {
            "respuesta": "Ok"
        }
        # return post_response_json
    except Exception as error:
        print("error en registrar_peticion",error)
        u.bitacora("error en registrar_peticion")
        return {
            "respuesta": "NoOk"
        }

def cargar_administradores():
    # u.bitacora(os.getenv("LIST_ADMIN"))
    lista = (os.getenv("LIST_ADMIN").split(","))
    ADMINISTRADORES = []
    for x in lista:
        ADMINISTRADORES.append(x)
    return ADMINISTRADORES

def cargar_autorizados():
    # u.bitacora(os.getenv("LIST_AUTORIZADOS"))
    lista = (os.getenv("LIST_AUTORIZADOS").split(","))
    AUTORIZADOS = []
    for x in lista:
        AUTORIZADOS.append(x)
    return AUTORIZADOS

def usuarioAdministrador(chat_id):
    ADMINISTRADORES = cargar_administradores()
    return str(chat_id) in ADMINISTRADORES

def usuarioAutorizado(chat_id):
    AUTORIZADOS = cargar_administradores()
    return str(chat_id) in AUTORIZADOS

def noAdministrador(bot, diractual, chat_id):
    sendChatAction(chat_id,'foto')
    foto = open(diractual+'/images/'+'nodata.gif', 'rb')
    bot.send_photo(chat_id, foto, 'No es administrador')

# def dirProxy():
#     # proxy = {
#     #     "https": FreeProxy(https=True).get()
#     # }
#     proxy = {
#         "https": "https://199.167.236.12:3128",
#         "https": "https://162.19.241.220:8091",
#         "https": "https://72.10.160.173:26173",
#     }
#     print(proxy)
#     return proxy
