'''
  File name: resumen.py
  Author: Cesar Cruz-A, Jonathan Olea-Z
  Project: ASR (Redes3) Configuracion de routers (modulo 3)
  Python Version: 2.7
'''
import datetime

from ftplib import FTP
import os.path
import subprocess

#dir_ip="192.168.2.1"
#local_file="Config"
#remote_file="startup-config"

#remote_user="rcp"
#remote_password="rcp"
#directorio="/"

url_orig="startup-config"; #url donde se recibe el archivo
url_dest="tftpboot/startup-config"; #url donde se dejara el archivo


def copyFile(ip, dir_origen, dir_destino, remote_user, remote_password): #remotamente copia el archivo de un directorio a otro
    try:
        dfg= subprocess.Popen(["sh", "copyFile.sh", ip, dir_origen, dir_destino, remote_user, remote_password], 
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE);
        response = dfg.communicate()
        #print(response);
        return 1    
    except subprocess.CalledProcessError as e:
        print e.output
        return 0

#remote_file es el archivo que debera estar en el router
def putFile(ip, rem_file, loc_file):    #recibe un archivo del directorio tftpboot con sh
    try:
        df= subprocess.check_output(["sh", "putFile.sh", ip, rem_file, loc_file]);
        return 1
    except subprocess.CalledProcessError as e:
        print e.output
        return 0

def getFile(ip, rem_file, loc_file):    #obtiene un archivo del directorio tftpboot con sh
    try:
        df= subprocess.check_output(["sh", "getFile.sh", ip, rem_file, loc_file]);
        return 1
    except subprocess.CalledProcessError as e:
        print e.output
        return 0

def getFile2(ip, rem_file, loc_file, remote_user, remote_password, directorio_rem):	#recibe un archivo del directorio tftpboot con ftpLib
    try: 
        now = datetime.datetime.now()
        marcaDeFecha=now.strftime("%Y-%m-%d_%H_%M_")

        ipSinPuntos = ip.replace(".", "_")   

        if not(os.path.exists(ipSinPuntos)):
            os.mkdir(ipSinPuntos)

        ftp=FTP(ip)
        ftp.login(remote_user, remote_password)
        ftp.cwd(directorio_rem)
        file=open(ipSinPuntos+'/'+marcaDeFecha+loc_file, 'wb')
        ftp.retrbinary('RETR '+rem_file, file.write)
        ftp.quit()
        print 'end'
        return 1
    except Exception,e:
        print e
        return 0

#hay una carpeta por cada direccion ip o por nombre del router?
def putFile2(ip, rem_file, loc_file, remote_user, remote_password, directorio_rem):	#envia un archivo del directorio tftpboot con ftpLib
    try: 
        ipSinPuntos = ip.replace(".", "_")      #para organizar los archivos        
        print ip
        ftp=FTP(ip)
        ftp.login(remote_user, remote_password)
        ftp.cwd(directorio_rem)
        file=open(ipSinPuntos+'/'+loc_file, 'rb')
        ftp.storbinary('STOR '+rem_file, file)
        ftp.quit()
        print 'end'
        return 1
    except Exception,e:
        print e
        return 0


#copyFile(dir_ip, url_orig, url_dest, remote_user, remote_password);

#putFile2("192.168.1.100", remote_file, local_file, "jonathan", "Samsung4660", directorio);
#print("sig comando");
#copyFile(dir_ip, url_dest, url_orig, remote_user, remote_password);


