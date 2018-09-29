import rrdtool
import time
import os
import sys
import datetime

from getSNMP import consultaSNMP
from notify import enviaAlerta

def procesarCadenaRetorno(cadena):
  cadena = cadena.lstrip()
  valor = cadena.split(" ")

  print "Valor: " + str(valor)

  try:
    float(valor[0])    
    return float(valor[0])
  except ValueError:    
    return 0

def creaBaseRRD(direccionIP):
  dirSinPuntos = direccionIP.replace(".","_")
  directorio = os.getcwd() + "/" + dirSinPuntos
  print "directorio" + directorio
  
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

  
def llenaBaseRRD(nombre, direccionIP, comunidad):
  #print "Nombre:"+nombre+" IP:"+direccionIP+" Comm:"+comunidad
  comunidad = comunidad.strip()
  dirSinPuntos = direccionIP.replace(".","_")
  directorio = os.getcwd() + "/" + dirSinPuntos
  i = 0

  while (1):
    i=i+1
    total_input_trafficICMP = int(
      consultaSNMP(comunidad, direccionIP,
             '1.3.6.1.2.1.5.1.0')) 
    total_output_trafficICMP = int(
      consultaSNMP(comunidad, direccionIP,
             '1.3.6.1.2.1.5.14.0'))

    total_input_trafficUDP = int(
      consultaSNMP(comunidad, direccionIP,
             '1.3.6.1.2.1.7.1.0')) 
    total_output_trafficUDP = int(
      consultaSNMP(comunidad, direccionIP,
             '1.3.6.1.2.1.7.4.0'))

    total_input_trafficTCP = int(
      consultaSNMP(comunidad, direccionIP,
             '1.3.6.1.2.1.6.10.0')) 
    total_output_trafficTCP = int(
      consultaSNMP(comunidad, direccionIP,
             '1.3.6.1.2.1.6.11.0'))

    total_input_trafficPING = int(
      consultaSNMP(comunidad, direccionIP,
             '1.3.6.1.2.1.5.9.0')) 
    total_output_trafficPING = int(
      consultaSNMP(comunidad, direccionIP,
             '1.3.6.1.2.1.5.22.0'))

    total_output_trafficTCP_Cons = int(
      consultaSNMP(comunidad, direccionIP,
             '1.3.6.1.2.1.6.9.0'))


    valor = "N:" + str(total_input_trafficICMP) + ':' + str(total_output_trafficICMP) + ':' \
        + str(total_input_trafficUDP) + ':' + str(total_output_trafficUDP) + ':' \
         + str(total_input_trafficTCP) + ':' + str(total_output_trafficTCP) + ':' \
          + str(total_input_trafficPING) + ':' + str(total_output_trafficPING) + ':' + str(total_output_trafficTCP_Cons) 

    # print "desde: "+direccionIP+" Valor: "+valor
    ret=rrdtool.update(directorio+"/net3.rrd", valor)
    rrdtool.dump(directorio+"/net3.rrd",directorio+"/net3.xml")
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
  
  dirSinPuntos = direccionIP.replace(".","_")
  directorio = os.getcwd() + "/" + dirSinPuntos
  print "DIRECTORIO --> " + directorio
  
  t = 1
  while (1):    
    print "fifo"
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
             "PRINT:entradaLAST:%6.2lf %SLAST")

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
             "PRINT:entradaLAST:%6.2lf %SLAST")

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
             "LINE2:outoctets#0000FF:Trafico de salida")

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
             "PRINT:salidaLAST:%6.2lf %SLAST")

    pingSalida = procesarCadenaRetorno(ret4[2][0])

    if pingSalida > 2:
      enviaAlerta("PING SALIDA POR ENCIMA DEL LIMITE", directorio+"/netPING.png")
      print "Enviare correo!!"


    ret5 = rrdtool.graph(directorio+"/netTCPc.png",
             "--start",str(tiempo_nuevo),
        #         "--end","N",
             "--title=Respuestas PING",  
             "--legend-direction=bottomup",
             "--vertical-label=Paq/s",
             "DEF:inoctets="+directorio+"/net3.rrd:outoctetsTCP_Cons:AVERAGE",
             "AREA:inoctets#F00F0F:PINGs de entrada")
	
    time.sleep(15)

