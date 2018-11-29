from ftplib import FTP
import time

def conectar_ftp(ip, user, passwd):
  ftp = FTP(ip)
  ftp.login(user, passwd)

  return ftp

def obtener_tiempo_de_respuesta_ftp(cliente_ftp):
	start = time.time()
	put_file(cliente_ftp, "archivoPrueba.txt")
	end = time.time()

	return str(end - start)

def put_file(cliente_ftp, archivo):
  try:         
    file = open(archivo, 'rb')
    cliente_ftp.storbinary('STOR ' + archivo, file)
    cliente_ftp.quit()
    return 1
  except Exception,e:
      print e
      return 0

def get_file(cliente_ftp, archivo): #recibe un archivo del directorio tftpboot con ftpLib
  try:         
    file = open(archivo, 'wb')
    cliente_ftp.retrbinary('RETR ' + archivo, file.write)
    cliente_ftp.quit()    
    return 1
  except Exception,e:
    print e
    return 0