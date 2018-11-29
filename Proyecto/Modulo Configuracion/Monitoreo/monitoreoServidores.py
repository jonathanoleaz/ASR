from multiprocessing.dummy import Pool as ThreadPool

from monitores.monitoreo_http import obtener_bytes_recibidos_http, obtener_tiempo_de_respuesta_http
from monitores.monitoreo_ftp import conectar_ftp, obtener_tiempo_de_respuesta_ftp
from monitores.monitoreo_ssh import obtener_conexiones_actuales, obtener_tiempo_conexion

IP_SSH = "192.168.0.8"
U_SSH = "servidores"
P_SSH = "12345678"

IP_HTTP = "192.168.0.8:8000"

def monitoreo(tipo_servidor):  
  if tipo_servidor == 0: # Servidor SSH       
    return ssh_monitoreo()
  elif tipo_servidor == 1: # Servidor FTP    
    return ftp_monitoreo()
  elif tipo_servidor == 2: # Servidor CUPS    
    return "Soy el servidor CUPS"
  elif tipo_servidor == 3: # Servidor SMTP    
    return "Soy el servidor SMTP"
  else:      
    return http_monitoreo()

def ssh_monitoreo():
  conexiones = obtener_conexiones_actuales(IP_SSH, U_SSH, P_SSH) # Se obtienen las conexiones actuales
  tiempos = obtener_tiempo_conexion(conexiones) # Se obtiene el tiempo de las conexiones previas
  respuesta = { "num_conexiones": len(conexiones), "tiempos_conexion": tiempos }

  return respuesta

def ftp_monitoreo():
  cliente_ftp = conectar_ftp(IP_SSH, U_SSH, P_SSH) # Conexion con cliente FTP
  tiempo_respuesta = obtener_tiempo_de_respuesta_ftp(cliente_ftp) # Se obtiene tiempo de respuesta
  
  return tiempo_respuesta

def http_monitoreo():
  print "TR-A"
  tiempo_respuesta = obtener_tiempo_de_respuesta_http(IP_HTTP) # Se obtiene tiempo de respuesta
  print "TR-D"
  print "CF-A"
  cliente_ftp = conectar_ftp(IP_SSH, U_SSH, P_SSH) # Conexion con cliente FTP
  print "CF-D"
  print "BR-A"
  bytes_recibidos = obtener_bytes_recibidos_http(cliente_ftp, IP_HTTP) # Se obtiene archivo pcap
  print "BR-D"
  respuesta = { "tiempo_respuesta": tiempo_respuesta, "bytes_recibidos": bytes_recibidos }

  return respuesta

def solicitudes_concurrentes(tipos):
  pool = ThreadPool(len(tipos)) # Se crea un pool de conexiones
  respuestas = pool.map(monitoreo, tipos) # Se ejecuta la funcion monitoreo
  pool.close() # Se cierra el pool de conexiones
  
  return respuestas

tipos_servidor = [0, 1, 2, 3, 4] # Lista para diferenciar el servidor
respuesta = solicitudes_concurrentes(tipos_servidor) # Se realizan las peticiones concurrentemente
print "Respuesta", respuesta
