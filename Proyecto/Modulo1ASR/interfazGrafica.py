'''
  File name: interfazGrafica.py
  Author: Cesar Cruz, Jonathan Olea
  Project: Adquisicion de datos
  Python Version: 2.7
'''
from Tkinter import *
from threading import Thread
from multiprocessing.dummy import Pool as ThreadPool

import tkMessageBox
import thread
import threading

from adquisicion.resumen import obtenerResumen
from adquisicion.agentesGrafico import agregarAgente, eliminarAgente
from adquisicion.masInf import mostrarMasInfo
from adquisicion.utilidadesRR import *

def hiloParaBaseRR(nombre,direccionIP,comunidad):
	creaBaseRRD(direccionIP)
	
	llenaBaseRRD(nombre,direccionIP,comunidad)
	return

def hiloParaGrafica(nombre,direccionIP):
	print("ya esta graficando")
	graficaRR(nombre, direccionIP)
	return

def worker(nombre, direccionIP, comunidad):
	
	s1 = Thread(target=creaBaseRRD, args=(direccionIP,))
	s1.start()
	s1.join()

	s2 = Thread(target=llenaBaseRRD, args=(nombre,direccionIP,comunidad,))
	s2.start()
	
	# time.sleep(5)
	# print "ya termino el hilo para la base"	
	s3 = Thread(target=graficaRR, args=(nombre, direccionIP,))
	s3.start()

	# thread.start_new_thread( hiloParaGrafica, (nombre,direccionIP,))	
	return

def obtenerResumenTODO():
	# Leo los agentes del archivo
	f = open("adquisicion/agentes.txt", "r")
	registros = f.readlines()
	f.close()
	datosAgentes = []
  
	# Se obtienen los todos los datos y se ponen en una lista
	for agente in registros:
		datosAgentes.append(agente.split(" "))

	# print datosAgentes
	return datosAgentes
	#funcion para obtener los elementos que no estan en una lista l1 pero en otra lista l2 si

def Diff(li1,li2):
	li_diff=[i for i in li1 + li2 if i not in li1 or i not in li2]
	return li_diff

#funcion que estara en el back revisando nuevos agentes en el txt para monitorearlos
def demonNuevosAgtes(datosAg):
	while(1):
		threads=[]	
		#print "El tipo de es"
		#print type(datosAg)
		datosAct=obtenerResumenTODO()
		nuevos=Diff(datosAg, datosAct)
		if(len(datosAg)<len(datosAct)):	
			print "Los nuevos fueron: "
			print nuevos
			i=0
			for aux in nuevos:
				#print(i)
				#print(str(aux[0])+"->"+str(aux[3]))
				t = threading.Thread(target=worker, args=(str(i),aux[0],aux[3]))
				threads.append(t)
				t.start()
				# print "ya se mandaron sus monitoreos"
				i=i+1
			for x in threads:
				x.join()
		datosAg=datosAct
		time.sleep(10);
	
def adquiereObjDeAgentes(nada):

  	tiempo_actual = int(time.time())
  	archivo=open("adquisicion/comienzo.txt",'w')

  	archivo.write(str(tiempo_actual))
  	archivo.close()

	threads = []
	i = 0

	while(i < 1):
#		print "vamos de nuevo"
		datosNec = obtenerResumenTODO()
		# print(datosNec)
		subproceso2 = Thread(target=demonNuevosAgtes, args=(datosNec,))
		subproceso2.start()

		for aux in datosNec:
			i = i + 1
			t = threading.Thread(target=worker, args=(str(i), aux[0],aux[3],))
			threads.append(t)
			t.start()

		for x in threads:
			x.join()
		i=i+1
	return

def verResumen():	
	# Se manda aviso del posible retardo de la solicitud
	tkMessageBox.showinfo("Aviso", "Este proceso toma unos segundos")
	clearVentana()

	# Para tener mas funcionalidades, se lanza un hilo para obtener dicho resumen (que igual usa hilos)
	pool = ThreadPool(1)
	resultados = pool.map(obtenerResumen, ".")	
	pool.close()
	pool.join()

	# Titulos que se agregaran a la ventana
	titulo = Label(root, text="Resumen de los agentes",  font='Helvetica 18 bold')
	titulo.pack()
	numAgentes = Label(root, text="Numero de agentes: " + str(len(resultados[0])),
	  font='Helvetica 14 bold')
	numAgentes.pack()
		
	# Se agregan la informacion de los agentes a la ventana
	for resultado in resultados[0]:
		muestraAgente(resultado)
    
def muestraAgente(agente):
	host = agente[0]

	# Se establece el valor de 'Down' o 'UP'
	if (host.values()[0] == 0): # Down
		hostL = Label(root, text="Host: " + host.keys()[0] + " (DOWN)", fg="red", font='Helvetica 14 bold')
		hostL.pack()
		return
	else: # Up
		numInt = agente[1]
		ints = agente[2:]
		hostL = Label(root, text="Host: " + host.keys()[0] + " (UP)", fg="green", font='Helvetica 14 bold')
		

	# Se establece el valor de 'Numero de Interfaces'
	intL = Label(root, text="\tNumero de Interfaces: " + str(numInt.values()[0]))	

	# Se checa el estado de las interfaces y se agrega a la ventana
	upInt = []
	downInt = []
	
	
	for itf in ints:		
		if (itf.values()[0] == '1'):
			upInt.append(itf.keys()[0])
		else:
			downInt.append(itf.keys()[0])				

	upIntL = Label(root, text="\tUP Interfaces: " + str(upInt))
	dwIntL = Label(root, text="\tDOWN Interfaces: " + str(downInt))

	hostL.bind("<Button-1>", lambda event, hostName=host.keys()[0]: masInformacion(hostName))
	hostL.pack()
	intL.pack()
	upIntL.pack()
	dwIntL.pack()

def masInformacion(hostName):
	mostrarMasInfo(hostName, root)

def clearVentana():
	# Se limpia la ventana
	list = root.pack_slaves()
	for l in list:
		l.destroy()

def agregaAgente():
	clearVentana()
	agregarAgente(root)

def eliminaAgente():
	clearVentana()
	eliminarAgente(root)


# Creacion de la ventana
root = Tk()

# Creacion de un menu
menubar = Menu(root)

# Creacion y configuracion de los item de Resumen
resumenMenu = Menu(menubar, tearoff=0)
resumenMenu.add_command(label="Ver resumen", command=verResumen)
menubar.add_cascade(label="Resumen", menu=resumenMenu)

# Creacion y configuracion de los item de Agente
agenteMenu = Menu(menubar, tearoff=0)
agenteMenu.add_command(label="Agregar agente", command=agregaAgente)
agenteMenu.add_command(label="Eliminar agente", command=eliminaAgente)
menubar.add_cascade(label="Agente", menu=agenteMenu)

# Creacion y configuracion de los item de Grafica
graficaMenu = Menu(menubar, tearoff=0)
graficaMenu.add_command(label="Ver Graficas")
menubar.add_cascade(label="Graficas", menu=graficaMenu)

# Correr metodo dentro de hilo para la adquisicion de datos de la mib de agentes
print "ya estoy adquiriendo datos"
subproceso = Thread(target=adquiereObjDeAgentes, args=("--",))
subproceso.start()

# Se agrega el menu
root.config(menu=menubar)
root.mainloop()


