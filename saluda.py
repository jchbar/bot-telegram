import time

tiempo = time.strftime('%H:%m:%S',time.localtime())
print('la hora es ',tiempo)
tiempoh = time.strftime('%H',time.localtime())
print('la hora es ',tiempoh)
if tiempoh < '12':
	saludo='Buenos dias'
elif tiempoh >= '12' and tiempoh < '18':
	saludo='Buenas tardes'
else:
	saludo='Buenas noches'
print(saludo)