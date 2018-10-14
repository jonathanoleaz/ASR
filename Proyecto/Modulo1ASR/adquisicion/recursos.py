import rrdtool
import subprocess

from getSNMP import consultaSNMP

OID_PROCESSOR_TABLE = '1.3.6.1.2.1.25.3.3.1.2'

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

def adicionInfoProcesadoresAgente(directorio, identificadores, comunidad, ipAddr):
  valores = "N:"
  for ide in identificadores: 
    ide = ide.replace('\n', '')   
    carga_CPU = int(consultaSNMP(comunidad, ipAddr, OID_PROCESSOR_TABLE + "." + ide))
    valores += str(carga_CPU) + ":"
  
  valores = valores[:-1]
  valores += ":0"
  print ipAddr + "->" + valores
  rrdtool.update(directorio + '/recursos.rrd', valores)
  # rrdtool.dump('trend1.rrd','trend.xml')
