import rrdtool
import time
import os
import sys
import datetime

from getSNMP import consultaSNMP
from notify import enviaAlerta
from recursos import *

LIM_ICMP = 100;
LIM_PING = 100;
LIM_UDP = 100;
LIM_TCP = 100;
LIM_TCPC = 100;

# OID's
INPUT_ICMP = '1.3.6.1.2.1.5.1.0'
OUTPUT_ICMP = '1.3.6.1.2.1.5.14.0'

def enviaCorreoSiEsMayor(valor, valorLimite, mensaje, rutaArchivo):
	if valor > valorLimite: # El valor excede lo esperado
		enviaAlerta(mensaje, rutaArchivo)		
	
def procesarCadenaRetorno(cadena):
  # Primero, se limpia la cadena
  cadena = cadena.lstrip()
  valor = cadena.split(" ")

  try:
    # Se convierte a un float
    float(valor[0])    
    return float(valor[0])
  except ValueError:    
    return 0

# Funcion que crea una BD de RRDtool por cada agente, dentro de una carpeta cuyo nombre es su IP
def creaBaseRRD(direccionIP, comunidad):
  dirSinPuntos = direccionIP.replace(".","_")			#Se quitan los puntos de la IP y se ponen _
  directorio = os.getcwd() + "/" + dirSinPuntos			#Se crea la cadena para la ruta relativa del directorio para cada agente,  
  
  if not os.path.exists(directorio):
    os.makedirs(directorio)
  
  ret = rrdtool.create(directorio + "/agente.rrd",
                     "--start",'N',
                     "--step",'15',
                     "DS:inoctetsICMP:COUNTER:600:U:U",
                     "DS:outoctetsICMP:COUNTER:600:U:U",
										 "DS:inoctetsUDP:COUNTER:600:U:U",
                     "DS:outoctetsUDP:COUNTER:600:U:U",
         						 "DS:inoctetsTCP:COUNTER:600:U:U",
                     "DS:outoctetsTCP:COUNTER:600:U:U",
										 "DS:inoctetsPING:COUNTER:600:U:U",
                     "DS:outoctetsPING:COUNTER:600:U:U",
										 "DS:outoctetsTCP_Cons:COUNTER:600:U:U",
                     "RRA:AVERAGE:0.5:1:600",
                     "RRA:AVERAGE:0.5:1:600",
										 "RRA:AVERAGE:0.5:1:600",
                     "RRA:AVERAGE:0.5:1:600",
           					 "RRA:AVERAGE:0.5:1:600",
                     "RRA:AVERAGE:0.5:1:600",
           					 "RRA:AVERAGE:0.5:1:600",
           	         "RRA:AVERAGE:0.5:1:600",
                     "RRA:AVERAGE:0.5:1:600")

  if ret:
    print rrdtool.error()

  # Creacion de la base de datos de recursos (procesador y memoria)
  # Primero, se debe de saber cuantos procesadores tiene el agente
  procesadores = obtenerProcesadores(comunidad, direccionIP)
  if len(procesadores) > 0: # Si se hace la base
    creacionBaseRecursos(directorio, len(procesadores))

    # Se obtienen los identificadores de los procesadores 
    identificadores = []
    for proc in procesadores:
      datos = proc.split('=')
      ident = datos[0].rstrip().split('.')[1]
      identificadores.append(ident)

    # Se hace un archivo para que lo pueda leer llenaBase & grafica
    proc_arch = open(directorio + "/procesadores.txt", "w")
    for ide in identificadores:
      proc_arch.write(ide + "\n")
    proc_arch.close()

#Funcion que va introducinedo en la BD de RRDtool los datos adquiridos por peticiones SNMP
def llenaBaseRRD(nombre, direccionIP, comunidad):  
  comunidad = comunidad.strip()				#Se quitan los caracteres de linea como \n \t \r de la cadena 
  dirSinPuntos = direccionIP.replace(".","_")		
  directorio = os.getcwd() + "/" + dirSinPuntos
  i = 0

  while (1):
    i = i + 1

    total_input_trafficICMP = int(
      consultaSNMP(comunidad, direccionIP, INPUT_ICMP)) 	#Paquetes ICMP de entrada
    total_output_trafficICMP = int(																#y de salida
      consultaSNMP(comunidad, direccionIP, OUTPUT_ICMP))	

    total_input_trafficUDP = int(
      consultaSNMP(comunidad, direccionIP,'1.3.6.1.2.1.7.1.0')) 	#Paquetes UDP de entrada y salida
    total_output_trafficUDP = int(
      consultaSNMP(comunidad, direccionIP,'1.3.6.1.2.1.7.4.0'))

    total_input_trafficTCP = int(
      consultaSNMP(comunidad, direccionIP,'1.3.6.1.2.1.6.10.0')) 	#Paquetes TCP de entrada y salida
    total_output_trafficTCP = int(
      consultaSNMP(comunidad, direccionIP,
             '1.3.6.1.2.1.6.11.0'))

    total_input_trafficPING = int(			
      consultaSNMP(comunidad, direccionIP,'1.3.6.1.2.1.5.9.0')) 	#Ecos ICMP (PINGs) de entrada y salida
    total_output_trafficPING = int(
      consultaSNMP(comunidad, direccionIP,'1.3.6.1.2.1.5.22.0'))

    total_output_trafficTCP_Cons = int(
      consultaSNMP(comunidad, direccionIP,'1.3.6.1.2.1.6.9.0'))		#Conexiones TCP establecidas


    valor = "N:" + str(total_input_trafficICMP) + ':' + str(total_output_trafficICMP) + ':' \
        + str(total_input_trafficUDP) + ':' + str(total_output_trafficUDP) + ':' \
         + str(total_input_trafficTCP) + ':' + str(total_output_trafficTCP) + ':' \
          + str(total_input_trafficPING) + ':' + str(total_output_trafficPING) + ':' + str(total_output_trafficTCP_Cons) 

    
    ret = rrdtool.update(directorio + "/agente.rrd", valor)			#Se actualiza la BD en los valores adquiridos via SNMP
    rrdtool.dump(directorio + "/agente.rrd", directorio + "/agente.xml")		#Se pondran los datos de la BD en tales archivos
    time.sleep(2)

    # Llenado de la base de recursos
    if os.path.exists(directorio + "/recursos.rrd"): # Tiene la base de recursos
      # Se obtienen los identificadores que estan en el archivo de procesadores
      proc_arch = open(directorio + "/procesadores.txt", "r")
      identificadores = proc_arch.readlines()

      # Se agrega la informacion del agente referente a recursos
      adicionInfoRecursosAgente(directorio, identificadores, comunidad, direccionIP)


  if ret:
    print rrdtool.error()
    time.sleep(300)
  
def graficaRR(nombre, direccionIP):
  tiempo_actual = int(time.time())
  tiempo_final = tiempo_actual - 86400
  tiempo_inicial = tiempo_final - 25920000
  archivo = open("adquisicion/comienzo.txt",'r')
  tiempo_nuevo = archivo.readline().strip()
  print tiempo_nuevo
  archivo.close()

  dirSinPuntos = direccionIP.replace(".","_")		#Se pasa la direccion IP con puntos a formato con "_"
  directorio = os.getcwd() + "/" + dirSinPuntos		#Se obtiene el directorio en el que deben guardarse las graficas .png
  
  t = 1
  while (1):        
    t = t + 1;
    ret = rrdtool.graph(directorio + "/netICMP.png",
             "--start",str(tiempo_nuevo),
        #         "--end","N",
             "--title=Trafico ICMP",  
             "--legend-direction=bottomup",
             "--vertical-label=Paq/s",
             "DEF:inoctets="+directorio+"/agente.rrd:inoctetsICMP:AVERAGE",
             "DEF:outoctets="+directorio+"/agente.rrd:outoctetsICMP:AVERAGE",
             "LINE2:inoctets#00FF00:Trafico de entrada",
             "LINE2:outoctets#0000FF:Trafico de salida",
						 "VDEF:entradaLAST=inoctets,LAST",
             "PRINT:entradaLAST:%6.2le LAST")

    value = procesarCadenaRetorno(ret[2][0])
    enviaCorreoSiEsMayor(value, LIM_ICMP, "ICMP por encima de"+str(LIM_ICMP), directorio+"/netICMP.png")    

    ret2 = rrdtool.graph(directorio+"/netUDP.png",
             "--start",str(tiempo_nuevo),
        #         "--end","N",
             "--title=Trafico UDP",  
             "--legend-direction=bottomup",
             "--vertical-label=Paq/s",
             "DEF:inoctets="+directorio+"/agente.rrd:inoctetsUDP:AVERAGE",
             "DEF:outoctets="+directorio+"/agente.rrd:outoctetsUDP:AVERAGE",
             "LINE2:inoctets#00FF00:Trafico de entrada",
             "LINE2:outoctets#0000FF:Trafico de salida",
             "VDEF:entradaLAST=inoctets,LAST",
             "PRINT:entradaLAST:%6.2le LAST")

    value = procesarCadenaRetorno(ret2[2][0])
    enviaCorreoSiEsMayor(value, LIM_UDP, "UDP por encima de"+str(LIM_UDP), directorio+"/netUDP.png")    

    ret3 = rrdtool.graph(directorio+"/netTCP.png",
             "--start",str(tiempo_nuevo),
        #         "--end","N",
             "--title=Trafico TCP",  
             "--legend-direction=bottomup",
             "--vertical-label=Paq/s",
             "DEF:inoctets="+directorio+"/agente.rrd:inoctetsTCP:AVERAGE",
             "DEF:outoctets="+directorio+"/agente.rrd:outoctetsTCP:AVERAGE",
             "LINE2:inoctets#00FF00:Trafico de entrada",
             "LINE2:outoctets#0000FF:Trafico de salida",
              "VDEF:entradaLAST=inoctets,LAST",
             "PRINT:entradaLAST:%6.2le LAST")

    value = procesarCadenaRetorno(ret3[2][0])
    enviaCorreoSiEsMayor(value, LIM_TCP, "TCP por encima de"+str(LIM_TCP), directorio+"/netTCP.png")

    ret4 = rrdtool.graph(directorio+"/netPING.png",
             "--start",str(tiempo_nuevo),
        #         "--end","N",
             "--title=Respuestas PING",  
             "--legend-direction=bottomup",
             "--vertical-label=Paq/s",
             "DEF:inoctets="+directorio+"/agente.rrd:inoctetsPING:AVERAGE",
             "DEF:outoctets="+directorio+"/agente.rrd:outoctetsPING:AVERAGE",
             "LINE2:inoctets#00FF00:PINGs de entrada",
             "LINE2:outoctets#0000FF:PINGs de salida",
             "VDEF:salidaLAST=outoctets,LAST",
             "PRINT:salidaLAST:%6.2le LAST")

    value = procesarCadenaRetorno(ret4[2][0])
    #if pingSalida > 2:
     # enviaAlerta("PING SALIDA POR ENCIMA DEL LIMITE", directorio+"/netPING.png")
     # print "Enviare correo!!"
    enviaCorreoSiEsMayor(value, LIM_PING, "PING por encima de"+str(LIM_PING), directorio+"/netPING.png")

    ret5 = rrdtool.graph(directorio+"/netTCPc.png",
             "--start",str(tiempo_nuevo),
        #         "--end","N",
             "--title=Conexiones ICMP",  
             "--legend-direction=bottomup",
             "--vertical-label=Con/s",
             "DEF:inoctets="+directorio+"/agente.rrd:outoctetsTCP_Cons:AVERAGE",
             "AREA:inoctets#F00F0F:Conexiones",
              "VDEF:salidaLAST=inoctets,LAST",
             "PRINT:salidaLAST:%6.2le LAST")

    value = procesarCadenaRetorno(ret5[2][0])
    enviaCorreoSiEsMayor(value, LIM_TCPC, "TCPconnections por encima de"+str(LIM_TCPC), directorio+"/netPING.png")
    
    # Graficado de recursos
    graficaRecursosAgente(directorio, tiempo_nuevo)

    # Tiempo de espera para hacer grafica
    time.sleep(15)

