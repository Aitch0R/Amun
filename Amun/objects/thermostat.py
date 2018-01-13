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
		obj.__init__(self,parent,info,preId,objid)
		#zero------------------------------------------------
		self.tState=0
		self.aState=0
		self.auto=0
		#-----------------------------------------------------

	def compose(self, to):
		if to=='agentS':#setup
			msg=self.index+',s,'#not needed till now
		elif to=='agent':#cmd
			msg=self.index+',0,'+str(self.tState)+',60'
		elif to=='client':
			msg=self.clientAddr+','+str(self.isActive)+','+str(self.auto)+','+str(self.aState)
		return msg
	
	def setState(self, state, typ):
		try:
			if state in ['0','1']:
				if typ=='t':
					self.tState=state
					self.agent.objCmd(self.compose('agent'))
				elif typ=='a':
					self.aState=state
		except ValueError:
			pass
		
	def process (self, _input):
		logger.debug(self.name +' process')
		try:
			self.setState(_input[0],'t')
			self.informAll()
		except ValueError: ##################correct error type
			pass
