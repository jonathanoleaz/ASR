from ftplib import FTP
import time

def obtener_tiempo_de_respuesta_ftp(ip, user, password):
	ftp = FTP(ip)
	ftp.login(user, password)

	start = time.time()
	ftp.cwd('/')
	end = time.time()

	return str(end - start)