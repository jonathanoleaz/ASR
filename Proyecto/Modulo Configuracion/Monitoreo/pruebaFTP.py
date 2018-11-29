from ftplib import FTP
import time

TARGET_IP = '192.168.0.8'
USERNAME = 'servidores'
PASSWORD = '12345678'

ftp = FTP(TARGET_IP)
ftp.login(USERNAME, PASSWORD)

start = time.time()
response = ftp.getwelcome()
end = time.time()

print end - start