from datetime import datetime
from datetime import timedelta
import spur
import pyshark

from monitoreo_ftp import get_file

PUERTO = 22
FMT = '%H:%M'
SSH_PCAP = "ssh.pcap"

def conectar_ssh(ip, user, password):
  shell_remoto = spur.SshShell(hostname=ip, 
    username=user, 
    password=password, 
    port=PUERTO,
    missing_host_key=spur.ssh.MissingHostKey.accept)

  return shell_remoto

def obtener_conexiones_actuales_ssh(ip, user, password):
  shell_remoto = conectar_ssh(ip, user, password)
  conexiones = shell_remoto.run(["who"]).output
  conexiones = conexiones.split("\n")[1:-1]  
  
  return conexiones

def obtener_tiempo_conexion_ssh(conexiones):
  tiempos = []
  fecha = datetime.now()
  hora_actual = str(fecha.hour) + ":" + str(fecha.minute)

  for conexion in conexiones:
    datos = conexion.split(" ")
    datos = list(filter(lambda dato: dato != '', datos))
    diferencia = datetime.strptime(hora_actual, FMT) - datetime.strptime(datos[3], FMT)
    tiempos.append(str(diferencia))
  
  return tiempos

def obtener_actividad_bytes_ssh(cliente_ftp, ssh_ip):
  get_file(cliente_ftp, SSH_PCAP) # Se obtiene el archivo  
  cap = pyshark.FileCapture(SSH_PCAP, only_summaries=True, keep_packets="True", display_filter="tcp")
  
  return obtener_totales(cap, ssh_ip)

def obtener_totales(cap, ssh_ip):
  total_enviado = 0
  total_recibido = 0

  try:
    for pkt in cap:
      if pkt.destination == ssh_ip:
        total_recibido += int(pkt.length)
      elif pkt.source == ssh_ip:
        total_enviado += int(pkt.length)
  except pyshark.capture.capture.TSharkCrashException as e:
    print e

  return total_enviado, total_recibido


