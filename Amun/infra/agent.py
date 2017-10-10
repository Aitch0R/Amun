#import
import importlib
import logging
import threading
import infra.config as config

wcom=importlib.import_module(config.wcom)

logger = logging.getLogger('mainLogger')
logger.info('agent: OK')
#---------------------------------------------------------------------

class agent(object):
	def __init__(self,info):
		self.port=dict(port=info['port'])
		self.logId='agent-'+str(self.port)+': '
		self.server=wcom.server(self,self.port)
		self.inmap={}
		self.objstring=''#place holder

	def insert(self,obj,key):
		self.inmap[key]=obj

	def process(self,caller,_input):
		try:
			self.inmap[_input[0]].aProcessor(_input[1:])
			'''self.inAdd=self.inmap[_input[0]].split(',')
			self.cInput=self.inAdd+_input[1:] #corrected input
			self.parent.process(self.cInput)'''
		except KeyError:
			logger.error('unknown dist')

	def objCmd(self, msg):
		self.server.send(msg)

	def statusUpdate(self,caller):
		pass

	def shutdown(self):
		self.server.shutdown()
