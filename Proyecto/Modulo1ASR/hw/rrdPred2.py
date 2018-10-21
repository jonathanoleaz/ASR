import time
import rrdtool

from getSNMP import consultaSNMP
from notify import enviaAlerta


total_input_traffic = 0
total_output_traffic = 0

NOMBRE_PNG="netP.png";
BASE_RRD="netPred.rrd";

VENTANA_CORREO=5;         #en caso que haya muchas aberraciones seguidas, enviara correos a lo mas, cada n minutos


init_time = rrdtool.last(BASE_RRD)		#para ventana: --start init_time_100
tiempo_actual = int(time.time())		        #sin ventana --start tiempo_actual

timeOfLastSentMail=int(time.time()-(60*VENTANA_CORREO)); #MUST BE this value for my condicional

                                                                                  # 3.6.1.2.1.2.2.1.10.10
while 1:
    total_input_traffic = int(consultaSNMP('pinguinos','localhost','1.3.6.1.2.1.2.2.1.10.2'))
    total_output_traffic = 0          #int(consultaSNMP('pinguinos','localhost','1.3.6.1.2.1.2.2.1.16.2'))

    valor = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
    print valor
    ret = rrdtool.update(BASE_RRD, valor)
    rrdtool.dump(BASE_RRD,'netP.xml')

    ret = rrdtool.graph(NOMBRE_PNG,
                        "--start", str(tiempo_actual),
			                  "--end", str(rrdtool.last(BASE_RRD)), #"--end", str(rrdtool.last('netPred.rrd') + 300),
                        "--vertical-label=Bytes/s",
			                  "--width", str(1000),
			                  "--height", str(500),
                        "DEF:obs="+BASE_RRD+":inoctets:AVERAGE",
                        "DEF:outoctets="+BASE_RRD+":outoctets:AVERAGE",
                        "DEF:pred="+BASE_RRD+":inoctets:HWPREDICT",
                        "DEF:dev="+BASE_RRD+":inoctets:DEVPREDICT",
                        "DEF:fail="+BASE_RRD+":inoctets:FAILURES",

                        #"VDEF:faill=fail,",
			                  "CDEF:faill=fail,1,*",

                        "CDEF:scaledobs=obs,8,*",
                        "CDEF:upper=pred,dev,2,*,+",
                        "CDEF:lower=pred,dev,2,*,-",
                        "CDEF:scaledupper=upper,8,*",
                        "CDEF:scaledlower=lower,8,*",
			                  "TICK:fail#FDD017:1.0:Fallas",
                        "LINE1:scaledobs#00FF00:In traffic",
                        #"LINE1:outoctets#0000FF:Out traffic",
                        "CDEF:scaledpred=pred,8,*",                   
                        "LINE2:scaledpred#ee0099:Prediction",
			"LINE1:scaledupper#FF000E:Upper",
			"LINE1:scaledlower#0012FF:Lower",
			"PRINT:faill:LAST:%0.0lf"
                        )

    t = time.localtime()          #legible para fecha normal
    tiempoNow = int(time.time())   #es mas facil manejar este para sacar la diferencia de n minutos
    
    print str(ret)+"->"+ret[2][0]
    print "Ventana: "+str(tiempoNow-timeOfLastSentMail);
    
    falla=0
    if(ret[2][0]!='-nan'):
      falla=int(ret[2][0])
      if(falla and (tiempoNow-timeOfLastSentMail > 60*VENTANA_CORREO)):   #si hay falla y el ultimo correo enviado fue hace 5 minutos
        enviaAlerta("Aberracion (comportamiento anormal) detectado a las: "+time.asctime(t), NOMBRE_PNG)
        timeOfLastSentMail=tiempoNow;
        print "email sent"

  #if valor > valorLimite: # El valor excede lo esperado
		#enviaAlerta(mensaje, rutaArchivo)

    time.sleep(1)

if ret:
    print rrdtool.error()
    time.sleep(300)
