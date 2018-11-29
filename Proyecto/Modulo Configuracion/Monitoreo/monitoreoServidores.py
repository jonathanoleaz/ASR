from multiprocessing.dummy import Pool as ThreadPool

from monitoreo_http import obtener_tiempo_de_respuesta_http
from monitoreo_ftp import obtener_tiempo_de_respuesta_ftp
from monitoreo_ssh import obtener_conexiones_actuales, obtener_tiempo_conexion

IP_SSH = "192.168.0.8"
U_SSH = "servidores"
P_SSH = "12345678"

def monitoreo(tipo_servidor):
  if tipo_servidor == 0: # Servidor SSH       
    return ssh_monitoreo()
  elif tipo_servidor == 1: # Servidor FTP
    return "FTP"  
    # return ftp_monitoreo()
  elif tipo_servidor == 2: # Servidor CUPS    
    return "Soy el servidor CUPS"
  elif tipo_servidor == 3: # Servidor SMTP    
    return "Soy el servidor SMTP"
  else:
    return "HTTP"
    # tiempo_respuesta = obtener_tiempo_de_respuesta_http('10.100.76.217:9999')   
    # return tiempo_respuesta

def ssh_monitoreo():
  conexiones = obtener_conexiones_actuales(IP_SSH, U_SSH, P_SSH)
  tiempos = obtener_tiempo_conexion(conexiones)
  respuesta = { "num_conexiones": len(conexiones), "tiempos_conexion": tiempos }

  return respuesta

def ftp_monitoreo():
  tiempo_respuesta = obtener_tiempo_de_respuesta_ftp('10.100.76.217', 'servidores', '12345678')
  return tiempo_respuesta


def solicitudes_concurrentes(tipos):
  pool = ThreadPool(len(tipos))
  respuestas = pool.map(monitoreo, tipos)
  pool.close()
  
  return respuestas

tipos_servidor = [0, 1, 2, 3, 4]
respuesta = solicitudes_concurrentes(tipos_servidor)
print "Respuesta", respuesta
