#import
import importlib
import logging
import threading
import infra.config as config

obj=importlib.import_module(config.obj).amunobj

logger = logging.getLogger('mainLogger')
logger.info(':OK') #######################################################change name
#---------------------------------------------------------------------
#relevants

class newObj(obj):
	def __init__(self,parent,info,objid):
		obj.__init__(self,parent,info,objid)
		#zero------------------------------------------------
		self.tStatus=0
		self.status=0
		#-----------------------------------------------------

	def compose(self, to):
		if to=='agentS':#setup
			msg=self.index+',s,'################################+'#something
		elif to=='agent':#cmd
			msg=self.index+',c,'###############################+'#something
		elif to=='client':
			msg=self.clientAddr+','+str(self.auto)+','######################+'#something
		return msg

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
		self.informAll()
