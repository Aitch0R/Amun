#import
import importlib
import logging
import threading
import infra.config as config

obj=importlib.import_module(config.obj).amunobj

logger = logging.getLogger('mainLogger')
logger.info('powerS:OK')
#------------------------------------------------------------------------------------------
class powerS(obj):
	def __init__(self,parent,info,objid):
		obj.__init__(self,parent,info,objid)
		self.clientAddr='5,'+str(self.objid)
		self.objstring=',,p,'+str(self.objid)+','+self.name
		#zero------------------------------------------------
		self.on=0
		#-----------------------------------------------------
	def statusUpdate(self,caller):
		pass

	def process (self, _input):
		logger.info('window process')
		try:
			if int(_input[0]) in [0,1]: #client -> mode, target
				self.auto=int(_input[0])
			else:
				pass #####################raise error
			self.blnabslvl(int(_input[1]),0)
			self.parent.objlists[0][0].update()############fix to do only when changing mode
			self.informAll()
		except ValueError: #correct error type
			pass

	def aProcessor(self, _input):
		self.feedback(int(_input[1]),int(_input[2]),int(_input[3]),int(_input[4]),int(_input[5]))
		self.informAll()
