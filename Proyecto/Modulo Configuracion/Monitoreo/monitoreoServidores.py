from multiprocessing.dummy import Pool as ThreadPool

from monitores.monitoreo_http import calcula_ancho_de_banda, obtener_bytes_recibidos_http, obtener_tiempo_de_respuesta_http
from monitores.monitoreo_ftp import conectar_ftp, obtener_tiempo_de_respuesta_ftp
from monitores.monitoreo_ssh import conectar_ssh, obtener_conexiones_actuales_ssh, obtener_tiempo_conexion_ssh, obtener_actividad_bytes_ssh
from monitores.monitoreo_cups import obtener_estado_impresoras

from monitores.monitoreo_smtp import *
from monitores.monitoreo_imap import *

IP_SMTP_IMAP="192.168.1.142"  #IP del servidor de correo electronico
IP_SSH = "192.168.1.143"
U_SSH = "servidores"
P_SSH = "12345678"

IP_HTTP = "192.168.1.143:8000"

def monitoreo(tipo_servidor):  
  if tipo_servidor == 0: # Servidor SSH       
    return ssh_monitoreo()
  elif tipo_servidor == 1: # Servidor FTP    
    return ftp_monitoreo()
  elif tipo_servidor == 2: # Servidor CUPS
    return cups_monitoreo()        
  elif tipo_servidor == 3: # Servidor SMTP    
    return correo_monitoreo()
  else:      
    return http_monitoreo()

def ssh_monitoreo():
  conexiones = obtener_conexiones_actuales_ssh(IP_SSH, U_SSH, P_SSH) # Se obtienen las conexiones actuales
  tiempos = obtener_tiempo_conexion_ssh(conexiones) # Se obtiene el tiempo de las conexiones previas
  cliente_ftp = conectar_ftp(IP_SSH, U_SSH, P_SSH) # Conexion con cliente FTP  
  bytes_enviados, bytes_recibidos = obtener_actividad_bytes_ssh(cliente_ftp, IP_SSH)

  respuesta = { "num_conexiones": len(conexiones),\
   "tiempos_conexion": tiempos, "bytes_enviados": bytes_enviados, "bytes_recibidos": bytes_recibidos  }

  return respuesta

def ftp_monitoreo():
  cliente_ftp = conectar_ftp(IP_SSH, U_SSH, P_SSH) # Conexion con cliente FTP
  tiempo_respuesta = obtener_tiempo_de_respuesta_ftp(cliente_ftp) # Se obtiene tiempo de respuesta
  
  return tiempo_respuesta

def http_monitoreo():  
  tiempo_respuesta = obtener_tiempo_de_respuesta_http(IP_HTTP) # Se obtiene tiempo de respuesta
  cliente_ftp = conectar_ftp(IP_SSH, U_SSH, P_SSH) # Conexion con cliente FTP  
  bytes_recibidos = obtener_bytes_recibidos_http(cliente_ftp, IP_HTTP) # Se obtiene archivo pcap
  #ancho_de_banda = calcula_ancho_de_banda(IP_SSH)
  ancho_de_banda = 1
  respuesta = { "tiempo_respuesta": tiempo_respuesta, "bytes_recibidos": bytes_recibidos, "ancho_de_banda": ancho_de_banda }

  return respuesta

def cups_monitoreo():
  ssh_remoto = conectar_ssh(IP_SSH, U_SSH, P_SSH)
  
  return obtener_estado_impresoras(ssh_remoto, IP_SSH)

def solicitudes_concurrentes(tipos):   
  pool = ThreadPool(len(tipos)) # Se crea un pool de conexiones
  respuestas = pool.map(monitoreo, tipos) # Se ejecuta la funcion monitoreo
  pool.close() # Se cierra el pool de conexiones
  
  return respuestas

def correo_monitoreo():
  tiempo_smtp = obtener_tiempo_de_respuesta_smtp(IP_SMTP_IMAP)
  tiempo_imap = obtener_tiempo_de_respuesta_imap(IP_SMTP_IMAP)
  #dl = borrar_correo_prueba(IP_SMTP_IMAP)
  respuesta= {"SMTP" : tiempo_smtp, "IMAP" : tiempo_imap}
  return respuesta


tipos_servidor = [0, 1, 2, 3, 4] # Lista para diferenciar el servidor
respuesta = solicitudes_concurrentes(tipos_servidor) # Se realizan las peticiones concurrentemente

ssh_r, ftp_r, cups_r, smtp_r, http_r = respuesta
print ".:: Servidor SSH ::."
print "\tConexiones activas:", ssh_r['num_conexiones']
print "\tTiempo de conexion:", ssh_r['tiempos_conexion']
print "\tBytes enviados:", ssh_r['bytes_enviados'], " bytes"
print "\tBytes recibidos:", ssh_r['bytes_recibidos'], " bytes"
print "\n"

print ".:: Servidor FTP ::."
print "\tTiempo de respuesta:", round(float(ftp_r), 6), "segundos con archivo de 2MB"
print "\n"

print ".:: Servidor CUPS ::."
print "\tNumero de impresoras: ", len(cups_r)
for impresora in cups_r:
  print "\t\tNombre:", impresora["nombre"], "--> Estado:", impresora["estado"]
print "\n"

print ".:: Servicio de correo ::."
print "\t Tiempos de respuesta: \n SMTP: ",smtp_r["SMTP"], "secs", "IMAP: ",smtp_r["IMAP"], "secs"
print "\n"

print ".:: Servidor HTTP ::."
print "\tTiempo de respuesta:", round(float(http_r['tiempo_respuesta']), 6), "segundos"
print "\tBytes recibidos:", http_r['bytes_recibidos'], "bytes"
print "\tVelocidad de descarga:", round(http_r['ancho_de_banda'], 3), "Mbps"