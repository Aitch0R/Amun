#import
import importlib
import logging
import threading
import infra.config as config

obj=importlib.import_module(config.obj).amunobj

logger = logging.getLogger('mainLogger')
logger.info(':thermostat')
#---------------------------------------------------------------------
#relevants

class thermostat(obj):
	def __init__(self,parent,info,preId,objid):
		obj.__init__(self,parent,info,objid)
		#zero------------------------------------------------
		self.stat=0
		self.auto=0
		#-----------------------------------------------------

	def compose(self, to):
		if to=='agentS':#setup
			msg=self.index+',s,'#not needed till now
		elif to=='agent':#cmd
			msg=self.index+','+str(self.tStatus)
		elif to=='client':
			msg=self.clientAddr+','+str(self.auto)+','+str(self.aStatus)
		return msg
	
	def setStat(self,stat):
		try:
			if stat in ['0','1']:
				self.stat=stat
				self.agent.objCmd(self.compose('agent'))
		except ValueError:
			pass
		
	def setAuto(self, stat):
		try:
			if stat in ['0','1']:
				self.auto=stat
		except ValueError:
			pass
		
	def setAState(self,stat):
		try:
			if stat in ['0','1']:
				self.aStat=stat
		except ValueError:
			pass
		
	def process (self, _input):
		logger.debug(self.name +' process')
		try:
			self.setAuto(_input[0])
			self.setState(_input[1])
			self.informAll()
		except ValueError: ##################correct error type
			pass
