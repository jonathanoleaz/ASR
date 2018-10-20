'''
  File name: notify.py
  Author: Cesar Cruz
  Project: Adquisicion de datos
  Python Version: 2.7
'''

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

mailsender = "mazetm182@gmail.com"
mailreceip = "cesar.cruz182@gmail.com"
mailserver = 'smtp.gmail.com: 587'
password = 'BATIZ1IM4'

def enviaAlerta(subject,imgPath):
    msg = MIMEMultipart()

    msg['Subject'] = subject
    msg['From'] = mailsender
    msg['To'] = mailreceip
    
    fp = open(imgPath, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    
    msg.attach(img)
    
    mserver = smtplib.SMTP(mailserver)
    mserver.starttls()
    # Login Credentials for sending the mail
    mserver.login(mailsender, password)

    mserver.sendmail(mailsender, mailreceip, msg.as_string())
    mserver.quit()
