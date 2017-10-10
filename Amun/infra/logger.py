import logging, logging.handlers
'''
class tcplog (logging.Handler):
	def emit(self, record):
		log_entry=self.format(record)
		print (log_entry)
		print ('loggggged')
'''
'''
# create logger with 'spam_application'
logger = logging.getLogger('mainLogger')
logger.setLevel(logging.DEBUG)
# create tcp handler which logs even debug messages
#sh = tcplog()
#sh.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('amun.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
longformat = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s: %(message)s')
shortformat=logging.Formatter('%(levelname)s: %(message)s')
fh.setFormatter(longformat)
ch.setFormatter(shortformat)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
#logger.addHandler(sh)
#---------------------------------------------------------------------------------------------------
comm = logging.getLogger('CommLogger')
comm.setLevel(logging.DEBUG)
fc = logging.FileHandler('amun_comm.log')
fc.setLevel(logging.DEBUG)
cc = logging.StreamHandler()
cc.setLevel(logging.DEBUG)
fc.setFormatter(longformat)
cc.setFormatter(shortformat)
comm.addHandler(fc)
comm.addHandler(cc)
'''
def logger(logName,logFile):
	print('creating logger')
	logger = logging.getLogger(logName)
	logger.setLevel(logging.DEBUG)
	fh = logging.FileHandler(logFile)
	fh.setLevel(logging.DEBUG)
	sh = logging.StreamHandler()
	sh.setLevel(logging.DEBUG)
	longformat = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s: %(message)s')
	shortformat=logging.Formatter('%(levelname)s: %(message)s')
	fh.setFormatter(longformat)
	sh.setFormatter(shortformat)
	logger.addHandler(fh)
	logger.addHandler(sh)



