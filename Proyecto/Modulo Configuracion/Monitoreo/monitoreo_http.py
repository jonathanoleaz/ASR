import requests

def obtener_tiempo_de_respuesta_http(ip):
	cadena_request = 'http://' + ip + '/'
	response = requests.get(cadena_request)
	return str(response.elapsed.total_seconds())