#probar.py
import json
msg = '''
{
    "update_id": 99200151,
    "message": {
        "message_id": 232,
        "from": {
            "id": 1691755707,
            "is_bot": false,
            "first_name": "Juan C",
            "last_name": "Hernandez B",
            "language_code": "es"
        },
        "chat": {
            "id": 1691755707,
            "first_name": "Juan C",
            "last_name": "Hernandez B",
            "type": "private"
        },
        "date": 1712931620,
        "text": "/ayuda",
        "entities": [
            {
                "offset": 0,
                "length": 6,
                "type": "bot_command"
            }
        ]
    }
}
'''
msg = json.loads(msg)

def clave_en_lista(msg, buscar):
    # lista = list(msg['message'].keys())
    # lista = json.loads(msg)
    lista = list(msg.keys())
    existe = False
    for llave in lista:
    	if llave==buscar:
    		existe=True
    		break
    # print ('buscar '+buscar+' en '+msg+ ' resultado ')
    # print(buscar in lista)
    # print(lista)
    # return buscar in lista
    print(lista)
    return existe


print (clave_en_lista(msg['message'],'entities'))
print (clave_en_lista(msg['message']['entities'][0],'type'))
# print (clave_en_lista(msg['message']['entities'][0]['type'],'bot_command'))
print (msg['message']['entities'][0]['type'])