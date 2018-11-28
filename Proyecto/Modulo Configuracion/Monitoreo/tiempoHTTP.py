import requests

ip = raw_input('Ingrese IP: ')
cadena_request = 'http://' + ip + '/'
response = requests.get(cadena_request)
print 'Tiempo de respuesta: ' + str(response.elapsed.total_seconds())