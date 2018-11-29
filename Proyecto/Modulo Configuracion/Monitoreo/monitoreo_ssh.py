from datetime import datetime
from datetime import timedelta
import spur

PUERTO = 2222
FMT = '%H:%M'

def obtener_conexiones_actuales(ip, user, password):
  shell_remoto = spur.SshShell(hostname=ip, 
    username=user, 
    password=password, 
    port=PUERTO,
    missing_host_key=spur.ssh.MissingHostKey.accept)
  conexiones = shell_remoto.run(["who"]).output
  conexiones = conexiones.split("\n")[1:-1]
  print "conexiones", conexiones
  
  return conexiones

def obtener_tiempo_conexion(conexiones):
  tiempos = []
  fecha = datetime.now()
  hora_actual = str(fecha.hour) + ":" + str(fecha.minute)

  for conexion in conexiones:
    datos = conexion.split(" ")
    datos = list(filter(lambda dato: dato != '', datos))
    diferencia = datetime.strptime(hora_actual, FMT) - datetime.strptime(datos[3], FMT)
    tiempos.append(str(diferencia))
  
  return tiempos
