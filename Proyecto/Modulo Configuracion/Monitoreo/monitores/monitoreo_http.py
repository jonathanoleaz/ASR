import requests
import pyshark

from monitoreo_ftp import get_file

HTTP_PCAP = "archivo.pcap"

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
