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
	def __init__(self,parent,info,objid):
		obj.__init__(self,parent,info,objid)
		#zero------------------------------------------------
		self.tStatus=0
		self.aStatus=0
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
	
	def setTStat(self,stat):
		try:
			if stat in ['0','1']:
				self.tStat=stat
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
			##############################fill here
			#####################raise error

			self.informAll()
		except ValueError: ##################correct error type
			pass

	def aProcessor(self, _input):
		#fill here
		self.setAState
		self.informAll()
