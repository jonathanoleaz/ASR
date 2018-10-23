import time
import rrdtool

from getSNMP import consultaSNMP
from notify import enviaAlerta

total_input_traffic = 0

NOMBRE_PNG = "netP.png"
BASE_RRD = "netPred.rrd"

VENTANA_CORREO = 1 # En caso que haya muchas aberraciones seguidas, enviara correos a lo mas, cada n minutos


init_time = rrdtool.last(BASE_RRD)    #para ventana: --start init_time_100
tiempo_actual = int(time.time())            #sin ventana --start tiempo_actual

timeOfLastSentMail = int(time.time() - (60 * VENTANA_CORREO)); #MUST BE this value for my condicional

OID = '1.3.6.1.2.1.2.2.1.10.3'
COMUNIDAD = 'public'
HOST = 'localhost'
                                                                                  # 3.6.1.2.1.2.2.1.10.10
while 1:
    total_input_traffic = int(consultaSNMP(COMUNIDAD, HOST, OID))          

    valor = "N:" + str(total_input_traffic)
    print valor
    ret = rrdtool.update(BASE_RRD, valor)
    rrdtool.dump(BASE_RRD, 'netP.xml')

    ret = rrdtool.graph(NOMBRE_PNG,
      "--start", str(tiempo_actual),
      "--end", str(rrdtool.last(BASE_RRD)), #"--end", str(rrdtool.last('netPred.rrd') + 300),
      "--vertical-label=Bytes/s",
      "--width=1000",
      "--height=500",
      "DEF:obs=" + BASE_RRD + ":inoctets:AVERAGE",                        
      "DEF:pred=" + BASE_RRD + ":inoctets:HWPREDICT",
      "DEF:dev=" + BASE_RRD + ":inoctets:DEVPREDICT",
      "DEF:fail=" + BASE_RRD + ":inoctets:FAILURES",                        
      "CDEF:faill=fail,1,*",
      "CDEF:scaledobs=obs,8,*",
      "CDEF:upper=pred,dev,2,*,+",
      "CDEF:lower=pred,dev,2,*,-",
      "CDEF:scaledupper=upper,8,*",
      "CDEF:scaledlower=lower,8,*",
      "TICK:fail#FDD017:1.0:Fallas",
      "LINE1:scaledobs#00FF00:In traffic",                        
      "CDEF:scaledpred=pred,8,*",                   
      "LINE2:scaledpred#ee0099:Prediction",
      "LINE1:scaledupper#FF000E:Upper",
      "LINE1:scaledlower#0012FF:Lower",
      "PRINT:faill:LAST:%0.0lf"
    )

    t = time.localtime() # Legible para fecha normal
    tiempoNow = int(time.time()) # Es mas facil manejar este para sacar la diferencia de n minutos
    
    #print str(ret) + "->" + ret[2][0]
    #print "Ventana: " + str(tiempoNow - timeOfLastSentMail)
    
    falla = 0
    if(ret[2][0] != '-nan'):
      falla = int(ret[2][0])

      if(falla and (tiempoNow-timeOfLastSentMail > 60 * VENTANA_CORREO)): # Si hay falla y el ultimo correo enviado fue hace 5 minutos
        enviaAlerta("Aberracion (comportamiento anormal) detectado a las: " \
          + time.asctime(t), NOMBRE_PNG)
        timeOfLastSentMail = tiempoNow;
        print "email sent"

    time.sleep(1)

if ret:
    print rrdtool.error()
    time.sleep(300)
