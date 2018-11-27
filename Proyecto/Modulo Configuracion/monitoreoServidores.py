from multiprocessing.dummy import Pool as ThreadPool

from monitoreo_http import obtener_tiempo_de_respuesta_http
from monitoreo_ftp import obtener_tiempo_de_respuesta_ftp


def monitoreo(tipo_servidor):
	if tipo_servidor == 0: # Servidor SSH				
		return "Soy el servidor SSH"
	elif tipo_servidor == 1: # Servidor FTP	
		tiempo_respuesta = obtener_tiempo_de_respuesta_ftp('localhost', 'servidores', '12345678')
		return tiempo_respuesta
	elif tipo_servidor == 2: # Servidor CUPS		
		return "Soy el servidor CUPS"
	elif tipo_servidor == 3: # Servidor SMTP		
		return "Soy el servidor SMTP"
	else:
		tiempo_respuesta = obtener_tiempo_de_respuesta_http('localhost:9999')		
		return tiempo_respuesta

def solicitudes_concurrentes(tipos):
	pool = ThreadPool(len(tipos))
	respuestas = pool.map(monitoreo, tipos)
	pool.close()
	
	return respuestas

tipos_servidor = [0, 1, 2, 3, 4]
respuesta = solicitudes_concurrentes(tipos_servidor)
print "Respuesta", respuesta