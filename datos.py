import utiles as u
'''
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
        print(url_post, new_data)
        post_response = requests.post(url_post, json=new_data)
        # Print the response
        post_response_json = post_response.json()
        # print(post_response_json)
        return post_response_json
        u.bitacora('sali solicitar_informacion  ')
    except Exception as error:
        print('error en solicitar_informacion',error)
        u.bitacora('error en solicitar_informacion')
        return {
            "respuesta": "NoOk"
        }
'''
def obtener_pregunta_hecha(msg):
    try:
        return msg["message"]["reply_to_message"]['text']
    except Exception as error:
        u.bitacora('error obtener_pregunta_hecha')

def eliminar_msg(chat_id, id_msg, bot):
    u.bitacora('entre eliminar_msg ')
    try:
        bot.delete_message(chat_id, id_msg)
        u.bitacora('sali eliminar_msg ')
    except Exception as error:
        print('no pude eliminar_msg',chat_id,id_msg,error)
        u.bitacora('no pude eliminar_msg '+str(chat_id + ' ' +str(id_msg)))

