#import
import importlib
import logging
import threading
import math
import infra.config as config

obj=importlib.import_module(config.obj).amunobj

logger = logging.getLogger('mainLogger')
logger.info('light:OK')
#---------------------------------------------------------------------

class light(obj):
	def __init__(self,parent,info,preId,objid):
		obj.__init__(self,parent,info,preId,objid)
		#zero--------------------
		self.actual=0
		self.target=0
		self.cmdid=0
		self.stufe=0
		self.frequency=200
		self.condition=None
		#------------------------

	def compose(self, to): ###specific
		if to=='agentS':#status request
			msg=str(self.cmdid)+',s'#############fix
		elif to=='agent':#cmd
			msg=self.index+',c,'+str(self.cmdid)+','+str(self.target)
		elif to=='client':
			msg=self.clientAddr+','+str(self.isActive)+','+str(self.auto)+','+str(self.actual)
		return msg

	#generate id for the cmd
	def cmdidgen(self): #specific
		if self.cmdid==9:
			self.cmdid=1
		else:
			self.cmdid=self.cmdid+1

	def rellevel(self,change): #specific
		if change > 0 and self.actual==100:
			pass #change to eliminate negative
		elif change < 0 and self.actual==0:
			pass
		else:
			self.parent.objlists[0][0].impact=True
			self.target=int(change*self.auto+self.actual)
			if self.target<0:
				self.target=0
			elif self.target>100:
				self.target=100
			logger.debug('shlvl '+str(self.target))
			self.cmdidgen()
			logger.debug(self.cmdid)
			self.abslevel(self.target,self.cmdid)
			self.condition=threading.Condition()
			self.condition.acquire()
			logger.debug('will wait')
			self.condition.wait(3)
			logger.debug('resume')
			self.condition.release()

	def abslevel(self,value,cmdid=0):#specific
		try:
			if value>= 0 and value <=100:
				self.target=value
				self.cmdid=cmdid
				self.agent.objCmd(self.compose('agent'))
			else:
				raise ValueError		
		except ValueError:
			logger.error('Value Error')
	
	#feedback from ESP of the actual level
	def feedback(self,cmdid,level): #convert to agentSideProcess
		if cmdid == 0:
			pass
		elif cmdid == self.cmdid:
			logger.debug('got'+str(cmdid))
			self.condition.acquire()
			self.condition.notify()
			logger.debug('notify')
			self.condition.release()
		else:
			logger.warning('nonmatching cmdid')
		try:
			if level>= 0 or level <=100:
				self.actual=level
				self.stufe=int(math.sqrt(self.actual))
			else:
				raise ValueError
		except ValueError:
			logger.error('Value Error')


	def statusUpdate(self,caller):#specific
		self.inform(caller)

	def shutdown(self): ##specific
		self.abslevel(0,0)
	
	def process(self, _input): #specific
		try:
			if int(_input[0]) in [0,1]: #client -> mode, target
				self.auto=int(_input[0])
			else:
				pass #####################raise error
			self.abslevel(int(_input[1]))
			self.parent.objlists[0][0].update()############fix to do only when changing mode
			self.informAll()
		except ValueError: #correct error type
			pass

	def aProcessor(self, _input): #specific #feedback -> cmdid, actual
		self.feedback(int(_input[0]),int(_input[1]))
		self.informAll()
#_____________________________________________________________________________________________________________
class rgb(obj):
	def __init__(self,parent,info,preId,objid):
		obj.__init__(self,parent,info,preId,objid)
		self.agents=self.parent.agents
		self.objlists=[0,0,[self.powerS]]
		self.R=light(self,dict(name=self.name+'-R',agent=self.info['agent'],agent_index=self.info['agent_index'],preStr='l',ps=0),0,0)
		self.G=light(self,dict(name=self.name+'-G',agent=self.info['agent'],agent_index=self.info['agent_indexG'],preStr='l',ps=0),0,1)
		self.B=light(self,dict(name=self.name+'-R',agent=self.info['agent'],agent_index=self.info['agent_indexB'],preStr='l',ps=0),0,2)
		self.tR=0
		self.tG=0
		self.tB=0

	def abscalc(self):
		self.R.abslevel(self.tR)
		self.G.abslevel(self.tG)
		self.B.abslevel(self.tB)

	def compose(self, to):
		if to=='agentS':#status request
			msg='obj,'+self.index+','+str(self.cmdid)+',s'#############fix
		elif to=='agent':#status request
			msg='obj,'+self.indexR+','+str(self.cmdid)+','+str(self.tR)+','+str(self.tG)+','+str(self.tB)
		elif to=='client':
			msg='2,'+str(self.objid)+','+str(self.isActive)+','+str(self.auto)+','+str(self.actual)+','+str(self.aRelR)+','+str(self.aRelG)+','+str(self.aRelB)
		return msg

	def feedback(self,cmdid,a,R,G,B):
		pass

	def process(self, _input):
		try:
			self.tR=int(_input[0])
			self.tG=int(_input[1])	
			self.tB=int(_input[2])
			self.abscalc()
			self.parent.objlists[0][0].update()
			self.pInformAll()
		except ValueError: ################correct error type
			pass
	
	def aProcessor(self, _input):
		self.feedback(int(_input[1]),int(_input[2]),int(_input[3]),int(_input[4]),int(_input[5]))
		self.informAll()

	def informAll(self,msg):
		pass

	def pInformall(self):
		pass
#_____________________________________________________________________________________________________________


