import spur

def obtener_estado_impresoras(ssh_remoto, ip_cups):
  respuesta = ssh_remoto.run(["lpstat", "-p"]).output
  estados = respuesta.split("\n")
  
  return procesamiento_estados(estados[:-1])

def procesamiento_estados(estados):
  estados_procesados = []
  for estado in estados:
    estados_procesados.append(obtener_info(estado))

  return estados_procesados

def obtener_info(estado):
  partes = estado.split(" ")  
  respuesta = {"nombre": partes[2], "estado": partes[4]}

  return respuesta