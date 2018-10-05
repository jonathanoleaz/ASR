import rrdtool
import time
import os
import sys
import datetime

from getSNMP import consultaSNMP
from notify import enviaAlerta

LIM_ICMP=100;
LIM_PING=100;
LIM_UDP=100;
LIM_TCP=100;
LIM_TCPC=100;

def enviaCorreoSiEsMayor(valor, valorLimite, mensaje, rutaArchivo):
	if valor > valorLimite:
		# enviaAlerta(mensaje, rutaArchivo)
		print valor
		print "Correo por"+mensaje
	

def procesarCadenaRetorno(cadena):
  cadena = cadena.lstrip()
  valor = cadena.split(" ")

  print "Valor: " + str(valor)

  try:
    float(valor[0])    
    return float(valor[0])
  except ValueError:    
    return 0

#Funcion que crea una BD de RRDtool por cada agente, dentro de una carpeta cuyo nombre es su IP
def creaBaseRRD(direccionIP):
  dirSinPuntos = direccionIP.replace(".","_")			#Se quitan los puntos de la IP y se ponen _
  directorio = os.getcwd() + "/" + dirSinPuntos			#Se crea la cadena para la ruta relativa del directorio para cada agente,
  #print "directorio" + directorio
  
  if not os.path.exists(directorio):
    os.makedirs(directorio)
  #  print "creado"
  
  ret = rrdtool.create(directorio + "/net3.rrd",
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

#Funcion que va introducinedo en la BD de RRDtool los datos adquiridos por peticiones SNMP
def llenaBaseRRD(nombre, direccionIP, comunidad):
  #print "Nombre:"+nombre+" IP:"+direccionIP+" Comm:"+comunidad
  comunidad = comunidad.strip()				#Se quitan los caracteres de linea como \n \t \r de la cadena 
  dirSinPuntos = direccionIP.replace(".","_")		
  directorio = os.getcwd() + "/" + dirSinPuntos
  i = 0

  while (1):
    i=i+1
    total_input_trafficICMP = int(
      consultaSNMP(comunidad, direccionIP,'1.3.6.1.2.1.5.1.0')) 	#Paquetes ICMP de entrada
    total_output_trafficICMP = int(																#y de salida
      consultaSNMP(comunidad, direccionIP,'1.3.6.1.2.1.5.14.0'))	

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

    # print "desde: "+direccionIP+" Valor: "+valor
    ret=rrdtool.update(directorio+"/net3.rrd", valor)			#Se actualiza la BD en los valores adquiridos via SNMP
    rrdtool.dump(directorio+"/net3.rrd",directorio+"/net3.xml")		#Se pondran los datos de la BD en tales archivos
    time.sleep(2)

  if ret:
    print rrdtool.error()
    time.sleep(300)
  
def graficaRR(nombre, direccionIP):
  
  tiempo_actual = int(time.time())
  tiempo_final = tiempo_actual - 86400
  tiempo_inicial = tiempo_final - 25920000
  archivo=open("adquisicion/comienzo.txt",'r')
  tiempo_nuevo=archivo.readline().strip()
  print tiempo_nuevo
  archivo.close()

  dirSinPuntos = direccionIP.replace(".","_")		#Se pasa la direccion IP con puntos a formato con "_"
  directorio = os.getcwd() + "/" + dirSinPuntos		#Se obtiene el directorio en el que deben guardarse las graficas .png
  #print "DIRECTORIO --> " + directorio
  
  t = 1
  while (1):    
    #print "fifo"
    t = t + 1;
    ret = rrdtool.graph(directorio+"/netICMP.png",
             "--start",str(tiempo_nuevo),
        #         "--end","N",
             "--title=Trafico ICMP",  
             "--legend-direction=bottomup",
             "--vertical-label=Paq/s",
             "DEF:inoctets="+directorio+"/net3.rrd:inoctetsICMP:AVERAGE",
             "DEF:outoctets="+directorio+"/net3.rrd:outoctetsICMP:AVERAGE",
             "LINE2:inoctets#00FF00:Trafico de entrada",
             "LINE2:outoctets#0000FF:Trafico de salida",
						 "VDEF:entradaLAST=inoctets,LAST",
             "PRINT:entradaLAST:%6.2le LAST")

    value = procesarCadenaRetorno(ret[2][0])
    enviaCorreoSiEsMayor(value, LIM_ICMP, "ICMP por encima de"+str(LIM_ICMP), directorio+"/netICMP.png")

    # print "Ret ->" + str(ret[2])

    ret2 = rrdtool.graph(directorio+"/netUDP.png",
             "--start",str(tiempo_nuevo),
        #         "--end","N",
             "--title=Trafico UDP",  
             "--legend-direction=bottomup",
             "--vertical-label=Paq/s",
             "DEF:inoctets="+directorio+"/net3.rrd:inoctetsUDP:AVERAGE",
             "DEF:outoctets="+directorio+"/net3.rrd:outoctetsUDP:AVERAGE",
             "LINE2:inoctets#00FF00:Trafico de entrada",
             "LINE2:outoctets#0000FF:Trafico de salida",
             "VDEF:entradaLAST=inoctets,LAST",
             "PRINT:entradaLAST:%6.2le LAST")

    value = procesarCadenaRetorno(ret2[2][0])
    enviaCorreoSiEsMayor(value, LIM_UDP, "UDP por encima de"+str(LIM_UDP), directorio+"/netUDP.png")
    # print "Ret2 ->" + str(ret[2])

    ret3 = rrdtool.graph(directorio+"/netTCP.png",
             "--start",str(tiempo_nuevo),
        #         "--end","N",
             "--title=Trafico TCP",  
             "--legend-direction=bottomup",
             "--vertical-label=Paq/s",
             "DEF:inoctets="+directorio+"/net3.rrd:inoctetsTCP:AVERAGE",
             "DEF:outoctets="+directorio+"/net3.rrd:outoctetsTCP:AVERAGE",
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
             "DEF:inoctets="+directorio+"/net3.rrd:inoctetsPING:AVERAGE",
             "DEF:outoctets="+directorio+"/net3.rrd:outoctetsPING:AVERAGE",
             "LINE2:inoctets#00FF00:PINGs de entrada",
             "LINE2:outoctets#0000FF:PINGs de salida",
             "VDEF:salidaLAST=outoctets,LAST",
             "PRINT:salidaLAST:%6.2le LAST")

    value = procesarCadenaRetorno(ret4[2][0])
    print "el valor del ret4 es: "
    print ret4
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
             "DEF:inoctets="+directorio+"/net3.rrd:outoctetsTCP_Cons:AVERAGE",
             "AREA:inoctets#F00F0F:Conexiones",
              "VDEF:salidaLAST=inoctets,LAST",
             "PRINT:salidaLAST:%6.2le LAST")

    value = procesarCadenaRetorno(ret5[2][0])
    enviaCorreoSiEsMayor(value, LIM_TCPC, "TCPconnections por encima de"+str(LIM_TCPC), directorio+"/netTCP.png")

	
    time.sleep(15)

