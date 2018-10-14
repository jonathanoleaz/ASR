'''
  File name: interfazGrafica.py
  Author: Cesar Cruz, Jonathan Olea
  Project: Adquisicion de datos
  Python Version: 2.7
'''
from datetime import date
from time import mktime

ONE_HR_POSIX = 86400 / 24
ONE_MIN_POSIX = ONE_HR_POSIX / 60

def realizar_prediccion(fecha_inicio, hora_inicio, fecha_termino, hora_termino,\
  agente, baseRRD, variable, limInf, limSup):  
  posix_inicio = calculo_fecha_posix(fecha_inicio, hora_inicio)
  posix_termino = calculo_fecha_posix(fecha_termino, hora_termino)
  """
  posix_fecha_inicio = mktime(fecha_inicio.timetuple())  
  hr_inicio, min_inicio = hora_inicio.split(":")
  h_inicio = (ONE_HR_POSIX * float(hr_inicio)) + (ONE_MIN_POSIX * float(min_inicio))
  posix_inicio = posix_fecha_inicio + h_inicio  
  
  # Calculo de posix_termino
  posix_fecha_termino = mktime(fecha_termino.timetuple())
  hr_termino, min_termino = hora_termino.split(":")
  h_termino = (ONE_HR_POSIX * float(hr_termino)) + (ONE_MIN_POSIX * float(min_termino))
  posix_termino = posix_fecha_termino + h_termino 
  """
  print 'Hr inicial: -> ' + str(posix_inicio)
  print 'Hr termino: -> ' + str(posix_termino)

def calculo_fecha_posix(fecha, hora):
  posix_fecha = mktime(fecha.timetuple())
  hr, mins = hora.split(":")
  posix_hora = (ONE_HR_POSIX * float(hr)) + (ONE_MIN_POSIX * float(mins))
  return posix_fecha + posix_hora 
  