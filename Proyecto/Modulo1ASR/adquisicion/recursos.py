'''
  File name: interfazGrafica.py
  Author: Cesar Cruz
  Project: Adquisicion de datos
  Python Version: 2.7
'''
import rrdtool
import subprocess
import random
import time

from getSNMP import consultaSNMP

OID_PROCESSOR_TABLE = '1.3.6.1.2.1.25.3.3.1.2'

OID_MEM_SIZE = '1.3.6.1.2.1.25.2.3.1.5'
OID_MEM_USED = '1.3.6.1.2.1.25.2.3.1.6'

def creacionBaseRecursos(directorio, num_procs):
  # Se procede a crear la base de datos round-robin
  datasources = []
  rra = []

  # Se generan los datasources de los procesadores
  for i in range(num_procs):
    dataStr = "DS:CPU" + str(i + 1) + "load:GAUGE:600:U:U" 
    datasources.append(dataStr)
    rraStr = "RRA:AVERAGE:0.5:1:600"
    rra.append(rraStr)

  # Se agrega el datasource de la memoria
  datasources.append("DS:Memory_Used:GAUGE:600:U:U")
  rra.append("RRA:AVERAGE:0.5:1:600")

  ret = rrdtool.create(directorio + "/recursos.rrd",
                     "--start",'N',
                     "--step",'15',
                     datasources, rra)

def obtenerProcesadores(comunidad, ipAddr):
  comunidad = comunidad.strip().lstrip()    
  snmpWalk = 'snmpwalk -v2c -c ' + comunidad + ' ' + ipAddr + ' ' + OID_PROCESSOR_TABLE

  # Se realiza la consulta
  try:
    retorno = subprocess.check_output(snmpWalk, shell=True)
    cargas = retorno.split('\n')
    cargas = cargas[:-1]

    return cargas
  except subprocess.CalledProcessError, e:
    return []

def adicionInfoRecursosAgente(directorio, identificadores, comunidad, ipAddr):
  valores = "N:"

  # Parte de informacion de procesadores
  for ide in identificadores: 
    ide = ide.replace('\n', '')   
    carga_CPU = int(consultaSNMP(comunidad, ipAddr, OID_PROCESSOR_TABLE + "." + ide))
    valores += str(carga_CPU) + ":"
  
  valores = valores[:-1]

  # Parte de informacion de memoria (RAM, en este caso (es por eso que tiene el 1))
  mem_size = int(consultaSNMP(comunidad, ipAddr, OID_MEM_SIZE + '.' + '1'))
  mem_used = int(consultaSNMP(comunidad, ipAddr, OID_MEM_USED + '.' + '1'))
  pct_used = int(float(mem_used) / float(mem_size) * 100)

  valores += ":" + str(pct_used)  
  rrdtool.update(directorio + '/recursos.rrd', valores)
  # rrdtool.dump('trend1.rrd','trend.xml')

def graficaRecursosAgente(directorio, tiempo_inicio):
  # Se lee el archivo, para saber cuantas graficas se haran
  proc_arch = open(directorio + "/procesadores.txt", "r")
  num_procs = len(proc_arch.readlines())

  # Se generan las propiedades de las graficas
  propiedades_recursos = []  

  # Primero los procesadores
  for i in range(num_procs):
    propiedades_recursos.append(generacionPropiedadesProcesadorGrafica(directorio, i, tiempo_inicio))

  # Propiedades para la memoria
  propiedades_recursos.append(generacionPropiedadesMemoriaGrafica(directorio, tiempo_inicio))

  # Se grafican todos los recursos
  for propiedad in propiedades_recursos:
    grafica(propiedad)

def generacionPropiedadesProcesadorGrafica(directorio, numProcesador, tiempo_inicio):
  propiedades = []
  grafica = directorio + "/recursos.rrd"

  # Cadenas relativas a la grafica de la linea
  definicion = "DEF:carga" + str(numProcesador + 1) + "=" + grafica + ":CPU" + str(numProcesador + 1) + "load:AVERAGE"
  color = "AREA:carga" + str(numProcesador + 1) + hex_code_colors() + ":CPU" + str(numProcesador + 1) + " load"
  
  # Se llena el arreglo con las propiedades
  propiedades.append(directorio + "/procesador" + str(numProcesador + 1) + ".png")
  propiedades.append("--start")
  propiedades.append(tiempo_inicio)  
  propiedades.append("--vertical-label=Carga CPU" + str(numProcesador + 1))  
  propiedades.append('--vertical-label')
  propiedades.append("Uso de CPU (%)")
  propiedades.append('--lower-limit=0')  
  propiedades.append('--upper-limit=100')
  propiedades.append('--rigid')
  propiedades.append(definicion)
  propiedades.append(color)

  return propiedades

def generacionPropiedadesMemoriaGrafica(directorio, tiempo_inicio):
  propiedades = []
  grafica = directorio + "/recursos.rrd"

  # Cadenas relativas a la grafica de la linea
  definicion = "DEF:Memory_Used=" + grafica + ":Memory_Used:AVERAGE"
  color = "AREA:Memory_Used" + hex_code_colors() + ":Memory_Used"
  
  # Se llena el arreglo con las propiedades
  propiedades.append(directorio + "/memoria.png")
  propiedades.append("--start")
  propiedades.append(tiempo_inicio)  
  propiedades.append("--vertical-label=Uso de Memoria")  
  propiedades.append('--vertical-label')
  propiedades.append("Uso de Memoria (%)")
  propiedades.append('--lower-limit=0')  
  propiedades.append('--upper-limit=100')
  propiedades.append('--rigid')
  propiedades.append(definicion)
  propiedades.append(color)

  return propiedades

def hex_code_colors():
  a = hex(random.randrange(0,256))
  b = hex(random.randrange(0,256))
  c = hex(random.randrange(0,256))
  a = a[2:]
  b = b[2:]
  c = c[2:]
  if len(a) < 2:
      a = "0" + a
  if len(b) < 2:
      b = "0" + b
  if len(c) < 2:
      c = "0" + c
  z = a + b + c
  return "#" + z.upper()

def grafica(propiedad):
  ret = rrdtool.graph(propiedad)