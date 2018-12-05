import smtplib
import time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

FROM = "jonathan@redes1.com"
TO = "cesar@redes1.com"


def obtener_tiempo_de_respuesta_smtp(ip):
	msg = MIMEMultipart()
	msg['From'] = FROM
	msg['To'] = TO
	msg['Subject'] = "Testing response time"

	body = "César Cruz Arredondo. Jonathan Olea Zuñiga --00--"
	msg.attach(MIMEText(body, 'plain'))

	server = smtplib.SMTP(ip, 25)
	server.login("jonathan@redes1.com", "12345")
	server.ehlo()
	#Send the mail
	text = msg.as_string()

	start = time.time()
	server.sendmail(FROM, TO, text)
	end = time.time()

	return end-start

#print "smpt response time: ",obtener_tiempo_de_respuesta_smtp('192.168.1.142'), " secs."
