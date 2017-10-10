import imaplib
import email
import subprocess
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

logger = logging.getLogger('Osiris')
logger.debug('OK')


usrnm= "h.a.behery@gmail.com"
psswrd= "1.4x.mah5ih"
toaddr = "aitch_ramesses@outlook.de"
mail = imaplib.IMAP4_SSL('imap.gmail.com')

def getmail():
	mail.login(usrnm , psswrd)
	logger.info('logged in')
	#Get messages from server:
	# Out: list of "folders" aka labels in gmail.
	mail.select("Narmer") # connect to label.
	status, response = mail.search(None, "UNSEEN")
	unread_msg_nums = response[0].split()
	# Print the count of all unread messages
	logger.info(len(unread_msg_nums))
	# '(FROM "%s")' % (sender_of_interest)
	# Print all unread messages from a certain sender of interest
	for e_id in unread_msg_nums:
		#_, response = mail.fetch(e_id, '(UID BODY[TEXT])')
		#da.append(response[0][1])
		result, data = mail.fetch(e_id, '(RFC822)')
		mesg = data [0][1]
		msg = email.message_from_string(mesg)
		sender = msg['From']
		subject = msg['Subject']
		if subject == 'run':
			logger.info('Run command')
			todo = msg.get_payload()[ 0 ].get_payload()
			cmd = str(todo)
			cmdls = cmd.split()
			logger.info(cmdls)
			p = subprocess.Popen(cmdls, stdout=subprocess.PIPE, shell=False)
			(output, err) = p.communicate()
			logger.info(output)
			sendmail(output)
			
			
	'''
	# Mark them as seen
	for e_id in unread_msg_nums:
		mail.store(e_id, '+FLAGS', '\Seen')
	'''


def sendmail(content):

	msg = MIMEMultipart()
	msg['From'] = "Osiris"
	msg['To'] = toaddr
	msg['Subject'] = "Osiris"
	logger.info('sending')

	'''
	filename = 'ail.txt'
	attachment = open('/home/aitch/Desktop/mail', "rb")
	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
	msg.attach(part)
	'''
	
	'''
	fp = open('/home/aitch/Desktop/mail.py' , 'rb')
	msg = MIMEText(fp.read())
	fp.close()
	'''
	
	body = str(content)
	msg.attach(MIMEText(body, 'plain'))
	
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(usrnm, psswrd )
	text = msg.as_string()
	server.sendmail(usrnm, toaddr, text)
	logger.info('sent')
	server.quit()
	



 



