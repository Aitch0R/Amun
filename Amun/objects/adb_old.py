import logging
import threading
import subprocess
import time

logger = logging.getLogger('Osiris')
logger.info('OK')

dctadb= dict(menu=1 ,home=3, back=4, up=19, down=20, left=21, right=22, center=23, volup=24, voldn=25, power=26, cmr=27, clear=28, space=62, ntr=66, delete=67, search=84, a=29, b=30, c=31, d=32, e=33, f=34, g=35, h=36, i=37, j=38, k=39, l=40, m=41, n=42, o=43, p=44, q=45, r=46, s=47, t=48, u=49, v=50, w=51, x=52, y=53, z=54)

class adb(object):
	def __init__(self,parent,info,objid,holder):
		self.info=info
		self.ip=self.info['ip']
		self.port=self.info['port']
		self.device=self.info['device']
		self.name=self.info['name']
		self.dct=dctadb
		self.monitor()
		self.connected=False
		self.objid=objid
		self.objstring=',,a,'+str(self.objid)+','+self.name

	def connect(self):
		self.msg="adb connect "+self.ip
		logger.info(self.msg)
		self.p = subprocess.Popen(self.msg.split(), stdout=subprocess.PIPE, shell=False)
		(self.output, self.err) = self.p.communicate()
		if 'connected' in self.output.decode():
			self.connected=True
			logger.info('connected to ADB: '+ self.ip)
		
	def key(self,_input):
			try:
				self.msg="adb -s device:"+self.device+" shell input keyevent "+str(self.dct[_input]) #fix txt #try except
			except KeyError:
				logger.error(_input+' is unknown')	
			self.p = subprocess.Popen(self.msg.split(), stdout=subprocess.PIPE, shell=False)
	
	'''def text(self,_input):
		self.txt=_input.split()
		for i in range(0,len(self.txt)):
			self.msg="adb -s device:"+self.device+" shell input text "+self.txt[i]
			self.p = subprocess.Popen(self.msg.split(), stdout=subprocess.PIPE, shell=False)
			time.sleep(.5)
			if i!=len(self.txt)-1:
				self.msg="adb -s device:"+self.device+" shell input keyevent 62"
				self.p = subprocess.Popen(self.msg.split(), stdout=subprocess.PIPE, shell=False)
				time.sleep(.3)'''
	def text(self,_input):
		self.txt=_input
		for i in range(0,len(self.txt)):
			if self.txt[i]==' ':
				self.msg="adb -s device:"+self.device+" shell input keyevent 62"
				self.p = subprocess.Popen(self.msg.split(), stdout=subprocess.PIPE, shell=False)
			else:
				try:
					self.msg="adb -s device:"+self.device+" shell input keyevent "+str(self.dct[self.txt[i]])
				except KeyError:
					logger.error(self.txt[i]+' is unknown')				
				self.p = subprocess.Popen(self.msg.split(), stdout=subprocess.PIPE, shell=False)
			time.sleep(0.3)

	def check (self):
		self.msg="adb devices -l"
		logger.info(self.msg)
		self.p = subprocess.Popen(self.msg, stdout=subprocess.PIPE, shell=False)
		(self.output, self.err) = self.p.communicate()
		if self.ip not in self.output.decode():
			self.connected=False
			self.connect()
			
	def monitor(self):
		self.c=threading.Timer(600,self.monitor)
		self.c.setDaemon(True)
		self.c.start()
		self.connect()

	def process(self,_input):
		try:
			if _input[0] == '1':
				self.key(_input[1])
			elif _input[0] == '2':
				threading.Thread(target=self.text,args=(_input[1],)).start()
		except IndexError:
			logger.error('wrong')

	def statusUpdate(self,caller):
		pass




'''
55 --> "KEYCODE_COMMA" 
56 --> "KEYCODE_PERIOD" 
57 --> "KEYCODE_ALT_LEFT" 
58 --> "KEYCODE_ALT_RIGHT" 
59 --> "KEYCODE_SHIFT_LEFT" 
60 --> "KEYCODE_SHIFT_RIGHT" 
61 --> "KEYCODE_TAB" 
80 --> "KEYCODE_FOCUS" 
82 --> "KEYCODE_MENU" 
83 --> "KEYCODE_NOTIFICATION"
''' 
