from ftplib import FTP
import time

def obtener_tiempo_de_respuesta_ftp(ip, user, password):
	ftp = FTP(ip)
	ftp.login(user, password)

	start = time.time()
	put_file(ftp, "archivoPrueba.txt")
	end = time.time()

	return str(end - start)

def put_file(ftp, archivo):
    try:         
      file = open(archivo, 'rb')
      ftp.storbinary('STOR ' + archivo, file)
      ftp.quit()
      return 1
    except Exception,e:
        print e
        return 0
