import random, re
txt_despedida = [
	'<b>Gracias</b> por usar este servicio, Su sesion se ha cerrado con exito',
	'Su sesion se ha cerrado con exito, <b>Gracias</b> por usar este servicio',
	'<b>Gracias</b> Ha sido un placer ayudarte',
	'Agradezco la oportunidad de haber sido de ayuda',
	'Ha sido genial ayudarte'
	]
for i in range(1,6):
	azar = random.randint(0,len(txt_despedida)-1)
	print(txt_despedida[azar])

