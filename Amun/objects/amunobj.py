import logging

class amunobj(object):
	def __init__(self,parent,info,preId,objid):
		self.parent=parent
		self.info=info
		self.preId=str(preId)
		self.preStr=self.info['preStr']
		self.name=self.info['name']
		self.objid=objid
		self.auto=0
		self.agent=self.parent.agents[self.info['agent']]
		self.index=str(self.info['agent_index'])
		self.agent.insert(self,self.index)
		self.clientAddr=self.preId+','+str(self.objid)
		self.objstring=',,'+self.preStr+','+str(self.objid)+','+self.name
		self.powerS=self.parent.objlists[2][self.info['ps']]
		self._standby=False
		self.isPowered=False
		self.powerS.enlist(self)
		self.isConnected=False
		self.isActive=0

	def status(self): #get status from agent by sending setup cmd
		self.agent.send(self.compose('agentS'))

	def powered(self, status):
		self._powered=status
		
		
	def standBy(self, status):
		print('standby func')
		if status in ['0', '1']:
			print('in true')
			self._standby=status
			self.powerS.check()

	def inform(self,caller): #inform caller
		caller.inform(str(self.parent.id)+','+self.compose('client'))
		
	#inform all users of the current status
	def informAll(self):
		self.parent.informAll(self.compose('client'))
	
	def connected(self,state):
		if state:
			self.isConnected=1
		else
			self.isConnected=0
		self.parent.informAll(self.compose('client'))
	
	def chkActive(self):
		self.agent.send('test')
		if isConnected and isPowered:
			self.temp=1
		else:
			self.temp=0
		if isActive not self.temp
			self.isActive=self.temp
			

	def process(self,_input):
		pass
	
	def aProcessor(self,_input):
		pass
