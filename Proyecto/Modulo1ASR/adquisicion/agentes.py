'''
  File name: agentes.py
  Author: Cesar Cruz, Jonathan Olea
  Project: Adquisicion de datos
  Python Version: 2.7
'''
import shutil

AGENTES_PATH = "adquisicion/agentes.txt"

def agregar():
  # Para consola 
  print ".:: Adicion de agentes ::."
  host = raw_input("Ingresa host o direccion IP: ")
  version = input("Version SNMP (1/2): ")
  puerto = input("Puerto: ")
  comunidad = raw_input("Comunidad: ")
  agregarAlArchivo(host, version, puerto, comunidad)

def eliminar():
  # Para consola
  print ".:: Remocion de agentes ::."
  host = raw_input("Ingrese host o direccion IP a eliminar: ")
  resultado = quitarDeArchivo(host)
  print "Resultado: " + str(resultado)

def agregarAlArchivo(host, version, puerto, comunidad):
  # Apertura del archivo
  f = open(AGENTES_PATH, "a")
  # Se escribe en el archivo
  f.write(host + " " + str(version) + " " + str(puerto) + " " + comunidad + '\r\n')
  # Se cierra descriptor
  f.close()

def quitarDeArchivo(host):
  # Apertura del archivo
  f = open(AGENTES_PATH, "r")
  # Se obtienen los agentes
  registros = f.readlines()
  # Se cierra, dado el mdodo.
  f.close()

  # Se vuelve a abrir, ahora para escribir
  f = open(AGENTES_PATH, "w")
  # Cursos al inicio
  f.seek(0)
  res = False

  # Se verifica cada registro que se tiene
  for agente in registros:    
    if (agente.split(" ")[0] == host): # Es el host?
      res = True
    else:
      f.write(agente)

  # Se cierra el descriptor
  f.close()
  shutil.rmtree(host.replace(".","_"), ignore_errors=True)
  return res
