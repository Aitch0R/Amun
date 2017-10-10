import imaplib
import email
import subprocess
import logging
module_logger = logging.getLogger('Osiris.module')

usrnm= "h.a.behery@gmail.com"
psswrd= "1.4x.mah5ih"
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(usrnm , psswrd)
logging.info('logged in')
#Get messages from server:
# Out: list of "folders" aka labels in gmail.
mail.select("Narmer") # connect to inbox.
status, response = mail.search(None, "ALL")
unread_msg_nums = response[0].split()

# Print the count of all unread messages
print len(unread_msg_nums)
# '(FROM "%s")' % (sender_of_interest)
# Print all unread messages from a certain sender of interest
da = []
for e_id in unread_msg_nums:
	#_, response = mail.fetch(e_id, '(UID BODY[TEXT])')
	#da.append(response[0][1])
	result, data = mail.fetch(e_id, '(RFC822)')
	mesg = data [0][1]
	msg = email.message_from_string(mesg)
	sender = msg['From']
	subject = msg['Subject']
	if subject == 'run':
		logging.info('Run command')
		todo = msg.get_payload()[ 0 ].get_payload()
		cmd = str(todo)
		cmdls = cmd.split()
		print cmdls
		logging.debug(cmdls)
		p = subprocess.Popen(cmdls, stdout=subprocess.PIPE, shell=False)
		(output, err) = p.communicate()
		print output
		#implement send response here
		p = subprocess.Popen(['python', '/home/aitch/Desktop/script_draft/send_imap.py', output], stdout=subprocess.PIPE, shell=False)
		
'''
# Mark them as seen
for e_id in unread_msg_nums:
	mail.store(e_id, '+FLAGS', '\Seen')
'''

