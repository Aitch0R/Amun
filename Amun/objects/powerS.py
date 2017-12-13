#import
import importlib
import logging
import threading
import infra.config as config

obj=importlib.import_module(config.obj).amunobj

logger = logging.getLogger('mainLogger')
logger.info('powerS:OK')

#---------------------------------------------------------------------
class powerS(obj):
	def __init__(self,parent,info,preId,objid):
		self.parent=parent
		self.info=info
		self.preId=str(preId)
		self.preStr=self.info['preStr']
		self.name=self.info['name']
		self.objid=objid
		self.agent=self.parent.agents[self.info['agent']]
		self.index=str(self.info['agent_index'])
		self.agent.insert(self,self.index)
		self.clientAddr=self.preId+','+str(self.objid)
		self.objstring='' #keep blank. not needed by app
		#zero------------------------------------------------
		self.attached=[]
		self.auto=1
		self.tStatus=0
		self.status=0
		#-----------------------------------------------------

	def compose(self, to):
		if to=='agentS':#setup
			msg=self.index+',s'
		elif to=='agent':#cmd
			msg=self.index+',0,'+str(self.tStatus)
		elif to=='client':
			msg=self.clientAddr+','+str(self.auto)+','+str(self.status)
		return msg

	def enlist(self,obj):
		self.attached.append(obj)

	def check(self):
		self.looping=True
		if self.auto==1:
			for obj in self.attached:
				if obj._standby=='1':
					self.tStatus=1
					self.looping=False
					break
				else:
					self.tStatus=0
			self.agent.objCmd(self.compose('agent'))

	def power(self, stats):
		try:
			if stats in [0,1]:
				self.tStatus=stats
			else:
				raise ValueError
			self.agent.objCmd(self.compose('agent'))
		except ValueError:
			#log
			pass


	def process (self, _input):
		logger.debug(self.name +' process')
		self.power(int(_input))

	def aProcessor(self, _input):
		try:
			if int(_input[1]) in [0,1]:
				print('ps got:'+_input[1])
				self.status=int(_input[1])
			else:
				raise ValueError
			self.informAll()
			self.informAttached()
		except ValueError:
			#log
			pass

	def informAttached(self):
		for obj in self.attached:
			obj.powered(self.status)
