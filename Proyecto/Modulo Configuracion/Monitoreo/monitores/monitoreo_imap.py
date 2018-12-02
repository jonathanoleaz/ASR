from imapclient import IMAPClient
import time

FROM = "jonathan@redes1.com"
TO = "cesar@redes1.com"

def obtener_tiempo_de_respuesta_imap(ip):
	server = IMAPClient(ip, port=143, ssl=False)
	server.login(TO, "12345")

	select_info = server.select_folder('INBOX')
	#print('%d messages in INBOX' % select_info[b'EXISTS'])

	start = time.time()
	messages = server.search(['SUBJECT', 'Testing response time'])
	end = time.time()
	#print (end-start)
	#print("%d messages from juan" % len(messages))

	for msgid, data in server.fetch(messages, ['ENVELOPE']).items():
		envelope = data[b'ENVELOPE']
		#print('ID #%d: "%s" received %s' % (msgid, envelope.subject.decode(), envelope.date))

	#for msgid, data in server.fetch(messages, ['INTERNALDATE', 'RFC822']).items():
	#	#envelope = data[b'ENVELOPE']
	#	print('ID #%d: "%s" received %s' % (msgid, envelope.subject.decode(), envelope.date))
	#	print(data)

	server.logout
	return end-start

def borrar_correo_prueba(ip):
  server = IMAPClient(ip, port=143, ssl=False)
  server.login(TO, "12345")

  select_info = server.select_folder('INBOX')
	#print('%d messages in INBOX' % select_info[b'EXISTS'])

  res = server.delete_messages(server.search(['SUBJECT', 'Testing response time']))
  res = server.expunge()

  server.logout
  return 0

#print obtener_tiempo_de_respuesta_imap('192.168.1.142')