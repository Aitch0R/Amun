#import
import importlib
import logging
import threading
import time
import infra.config as config

wcom=importlib.import_module(config.wcom)
adb=importlib.import_module(config.adb).adb
light=importlib.import_module(config.light)
window=importlib.import_module(config.window)
ir=importlib.import_module(config.ir)
powerS=importlib.import_module(config.powerS)
irrcv=importlib.import_module(config.irrcv)

logger = logging.getLogger('mainLogger')
logger.info('room:OK')
#---------------------------------------------------------------------------------------
class room(object):
	def __init__(self,lists,index,agentrep):
		#parameters---------------------------------------------------------------------
		#room---------------------------------------------------------------------------
		self.id=index
		self.autopilot=True
		self.agentrep=agentrep #repository
		self.lists=lists
		self.info=self.lists['info']
		self.name=self.info['name']
		logger.info(self.name+' created')
		#list---------------------------------------------------------------------------
		self.users=[]
		self.agents=self.agentrep
		self.lights=[]
		self.windows=[]	
		self.irs=[]
		self.adbs=[]
		self.powerSs=[]
		self.regulators=[]
		self.sensors=[]
		self.objlists=[self.regulators, self.agents, self.powerSs, self.lights, self.windows, self.irs, self.adbs, self.sensors]
		
		#communication______________________________________________________________________
		#self._agents=self.lists['agents']
		#for self._agent in self._agents:
		#	self.agents.append(self.agentrep[_agent])			
			
		#objects #args erst bei __init__()__________________________________________________
		self._objects=self.lists['objects']
		for self._object in self._objects: #_window1=['window','window1',1]

			self._object['preStr']=None #reset to avoid false assignment in case of unrecognised objects
			self.preId=None
			self.objClass=None
			
			if self._object['typ'] == 'light':
				self._object['preStr']='l'
				self.preId=3	# index of the list the object will be inserted in
				if self._object['cls'] == 1:
					self.objClass=light.light
				elif self._object['cls'] == 2:
					self.objClass=light.rgb
				
			elif self._object['typ'] == 'window':
				self._object['preStr']='w'
				self.preId=4
				self.objClass=window.window
				
			elif self._object['typ'] == 'ir':
				self._object['preStr']='ir'
				self.preId=5
				self.objClass=ir.ir
				#self.objid=str(len(self.ir))
				#self.ir.append(ir.ir(self,self._object,self.objid))

			elif self._object['typ'] == 'adb':
				self._object['preStr']='a'
				self.preId=6
				self.objClass=adb
				#self.objid=str(len(self.adb))
				#self.adb.append(adb(self,self._object,self.objid))

			elif self._object['typ'] == 'powersupply':
				self._object['preStr']='ps'
				self.preId=2
				self.objClass=powerS.powerS

			elif self._object['typ'] == 'irsensor':
				self._object['preStr']='irrcv'
				self.preId=7
				self.objClass=irrcv.ir_rcv

#			try:
			self.objlists[self.preId].append(self.objClass(self,self._object,self.preId,str(len(self.objlists[self.preId]))))
#			except TypeError:
#				logger.info('unknown')
				
		#regulators______________________________________________________________________
		self.regulators.append(brightness_regulator(self))
		self.regulators.append(temperature_regulator(self))

		self.roomstring=',,,'+str(self.id)+','+self.name
		for objList in self.objlists:		
			for obj in objList:
				self.roomstring=self.roomstring+obj.objstring

	def adduser(self,user):
		self.users.append(user)
		logger.info(user.name+' added to '+self.name)

	def informAll (self, msg):
		self.nmsg=str(self.id)+','+msg
		for user in self.users:
				user.inform(self.nmsg)

	#______________________________________________________________________________
	def process(self,caller,_input):#try
		try:
			self.objlists[int(_input[0])][int(_input[1])].process(_input[2:])
		except IndexError:
			logger.error('Index Error')

	def statusUpdate(self,caller):
		for objList in self.objlists:
			for obj in objList:
				obj.statusUpdate(caller)
		
		
		
	def shutdown(self, total):#shut all objects?
		for i in self.agents:
			i.shutdown()
		if total:#total shutdown
			for objList in self.objlists:
				for obj in objList:
					obj.shutdown()
#______________________________________________________________________________________________
class brightness_regulator(object):
	def __init__(self, parent):
		self.parent=parent
		self.enabled=0 #0,1
		self.lights=self.parent.lights
		self.windows=self.parent.windows
		self.agent=self.parent.agents[parent.lists['sensors'][0]['agent']]#2bcorrected
		self.agent.insert(self,'0')
		self._brightness_actual=0
		self._brightness_target=0
		self._brightness_tolerance=3
		self.mode='1' #1-light, 2-weight
		self.brightness_block=False
		self.factor=1 #experementary
		self.logger_id=self.parent.name+': '
		self.update()
		self.impact=False
		self.objstring=''	#place holder
		#self.reqbrightness()
		

	@property
	def weight(self):
		return self.lightweight
	@weight.setter
	def weight(self, weight):
		try:
			if weight<0 or weight>100:
				raise ValueError
			self.lightweight=weight
			self.windowweight=100-self.lightweight
			logger.debug(self.logger_id+'lightweight='+str(self.lightweight))
		
		except ValueError:
			logger.error(self.logger_id+'Value Error')

	@property
	def brightness_actual(self):
		return self._brightness_actual
	@brightness_actual.setter
	def brightness_actual(self, value):
		try:
			if value<0 or value>100:
				raise ValueError
			self._brightness_actual=value
			logger.info(self._brightness_actual)
			#self.parent.informAll('0,0,a,'+str(self._brightness_actual))
			logger.debug(self.logger_id+'actual brightness='+str(self._brightness_actual))
			self.brightness_reg()
		except ValueError:
			logger.error(self.logger_id+'Value Error')

	@property
	def brightness_target(self):
		return self._brightness_target
	@brightness_target.setter
	def brightness_target(self, value):
		try:
			if value<0 or value>100:
				raise ValueError
			self._brightness_target=value
			logger.debug(self.logger_id+'target brightness='+str(self._brightness_target))
			self.brightness_reg()
		except ValueError:
			logger.error(self.logger_id+'Value Error')

	def state(self,value):
		if value==0:
			self.enabled=0
			logger.info(self.logger_id+'brightness regulator disabled')
		elif value==1:
			self.enabled=1
			logger.info(self.logger_id+'brightness regulator enabled')
		
	
	def update(self):
		self.summ=0
		if self.mode=='1':
			
			for obj in self.lights:
				self.summ=self.summ+obj.auto
		
		if self.mode=='2':
			for obj in self.window:
				self.summ=self.summ+obj.weight

	def brightness_reg(self):
		if self.enabled==1 and not self.brightness_block and self.summ!=0:
			self.impact=False
			logger.debug(self.summ)
			self.brightness_block=True #block calling the thread
			self.brightness_diff=self._brightness_target-self._brightness_actual
			if abs(self.brightness_diff)>self._brightness_tolerance:
				#regulator options
				self.unit=self.brightness_diff*self.factor/self.summ
				self.orderlist=[]
				if self.lightweight!=0:
					logger.debug('sending to light')
					for obj in self.lights:
						logger.debug('actual:'+str(self._brightness_actual)+'target:'+str(self._brightness_target))
						logger.debug(self.unit)
						self.order=threading.Thread(target=obj.rellevel,args=(self.unit*self.lightweight,),)
						logger.debug('sent')
						self.orderlist.append(self.order)
						self.order.start()
						#wait for it
				if self.windowweight!=0:
					logger.debug('regulating window')
					for obj in self.windows:						
						self.order=threading.Thread(target=obj.rellvl,args=(self.unit*self.windowweight,),)
						logger.debug('sent')
						self.orderlist.append(self.order)
						self.order.start()
						#wait for it
				logger.debug(self.logger_id+'regulator waiting')
				for order in self.orderlist:
					logger.debug(self.logger_id+'join here')
					order.join()
				if self.impact:
					self.reqbrightness()
			self.brightness_block=False
			logger.debug(self.logger_id+'reg finished all')
			'''
				if self.windowweight!=0:
					for obj in self.window:
						obj.setval(unit)
						#wait for it'''
				
	def reqbrightness(self):
		self.agent.send('0')

	def informAll(self):
		self.msg='0,0,'+str(self.enabled)+','+str(self._brightness_actual)+','+str(self._brightness_target)+','+self.mode
		self.parent.informAll(self.msg)

	def inform(self,caller):
		self.msg='0,0,'+str(self.enabled)+','+str(self._brightness_actual)+','+str(self._brightness_target)+','+self.mode
		caller.inform(self.msg)

	def statusUpdate(self,caller):
		self.inform(caller)

	def process(self,_input):#try me
			if _input[0]=='a':
				self.brightness_actual=int(_input[1])
				logger.debug('room process brightness actual')
			elif _input[0]=='t':
				self.brightness_target=int(_input[1])
				logger.debug('room process brightness should')
			elif _input[0]=='l':
				self.brightness_tolerance=int(_input[1])
				logger.debug('room process brightness tolerance')
			elif _input[0]=='w':
				self.weight=int(_input[1])
				self.update
				logger.debug('room process brightness actual')	
			elif _input[0]=='s':
				self.state(int(_input[1]))
			#self.informAll()

	def aProcessor(self,_input):#try me
#		self.brightness_actual=int(_input[2])
#		self.informAll() ###############################suspended till fixing the range
		pass
#______________________________________________________________________________
class temperature_regulator(object):
	def __init__(self,parent):
		self.temperature_actual=20
		self.temperature_target=20
		self.objstring='' #place holder

	def statusUpdate(self,caller):
		pass
