import requests
import pyshark
import time

from monitoreo_ftp import get_file
from getSNMP import consultaSNMP

HTTP_PCAP = "http.pcap"
OID_INOCTETS = "1.3.6.1.2.1.2.2.1.10.2"
OID_OUTOCTETS = "1.3.6.1.2.1.2.2.1.16.2"
OID_SPEED = "1.3.6.1.2.1.2.2.1.5.2"
COMUNIDAD = "public"
DELTA = 2.0

def obtener_tiempo_de_respuesta_http(ip):
  cadena_request = 'http://' + ip + '/' # Cadena para realizar el GET  
  response = requests.get(cadena_request) # Se realiza el GET    

  return str(response.elapsed.total_seconds()) # Se retorna el tiempo

def obtener_bytes_recibidos_http(cliente_ftp, http_ip):  
  get_file(cliente_ftp, HTTP_PCAP) # Se obtiene el archivo  
  cap = pyshark.FileCapture(HTTP_PCAP, only_summaries=True, keep_packets="True", display_filter="http")
  
  return obtener_total_recibido(cap, http_ip) # Se retorna la cantidad total de bytes 
  
def obtener_total_recibido(cap, http_ip):
  total = 0
  try:
    for pkt in cap:
      if pkt.destination == http_ip.split(":")[0]:
        total += int(pkt.length)
  except pyshark.capture.capture.TSharkCrashException as e:
    print e

  return total

def calcula_ancho_de_banda(ip):
  in1 = consultaSNMP(COMUNIDAD, ip, OID_INOCTETS)
  out1 = consultaSNMP(COMUNIDAD, ip, OID_OUTOCTETS)
  vel1 = consultaSNMP(COMUNIDAD, ip, OID_SPEED)  
  time.sleep(DELTA)
  in2 = consultaSNMP(COMUNIDAD, ip, OID_INOCTETS)
  out2 = consultaSNMP(COMUNIDAD, ip, OID_OUTOCTETS)
  vel2 = consultaSNMP(COMUNIDAD, ip, OID_SPEED)

  delta_in = int(in2) - int(in1)
  delta_out = int(out2) - int(out1)  
  ancho_de_banda = ((delta_in + delta_out) * 800.0) / (DELTA * int(vel2))  

  return ancho_de_banda
