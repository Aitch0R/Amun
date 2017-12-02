import logging
import threading
import subprocess
import time
import importlib
import infra.config as config

wcom=importlib.import_module(config.wcom)

logger = logging.getLogger('Osiris')
logger.info('OK')

#dctadb= dict(menu=1 ,home=3, back=4, up=19, down=20, left=21, right=22, center=23, volup=24, voldn=25, power=26, cmr=27, clear=28, space=62, ntr=66, delete=67, search=84, a=29, b=30, c=31, d=32, e=33, f=34, g=35, h=36, i=37, j=38, k=39, l=40, m=41, n=42, o=43, p=44, q=45, r=46, s=47, t=48, u=49, v=50, w=51, x=52, y=53, z=54)

class adb(object):
	def __init__(self,parent,info,preId,objid):
		self.info=info
		self.ip=self.info['ip']
		self._port=self.info['port']
		self.device=self.info['device']
		self.name=self.info['name']
#		self.dct=dctadb
		self.connected=False
		self.objid=objid
		self.objstring=',,a,'+str(self.objid)+','+self.name
		self.port=wcom.port(self,dict(ip=self.ip, port=self._port))
		self.connect()

	def connect(self):
		self.port.up()
		self.firstContact()

	def firstContact(self):
		self.port.send(b'CNXN\x00\x00\x00\x01\x00\x10\x00\x00\x07\x00\x00\x002\x02\x00\x00\xbc\xb1\xa7\xb1host::\x00')
		
	def key(self,_input):
			try:
				self.port.send(dictadb[_input]) #fix txt #try except
			except KeyError:
				logger.error(_input+' is unknown')	
			#self.p = subprocess.Popen(self.msg.split(), stdout=subprocess.PIPE, shell=False)
	
#	def text(self,_input):
#		self.txt=_input.split()
#		for i in range(0,len(self.txt)):
#			self.msg="adb -s device:"+self.device+" shell input text "+self.txt[i]
#			self.p = subprocess.Popen(self.msg.split(), stdout=subprocess.PIPE, shell=False)
#			time.sleep(.5)
#			if i!=len(self.txt)-1:
#				self.msg="adb -s device:"+self.device+" shell input keyevent 62"
#				self.p = subprocess.Popen(self.msg.split(), stdout=subprocess.PIPE, shell=False)
#				time.sleep(.3)

#	def text(self,_input):
#		self.txt=_input
#		for i in range(0,len(self.txt)):
#			if self.txt[i]==' ':
#				self.msg="adb -s device:"+self.device+" shell input keyevent 62"
#				self.p = subprocess.Popen(self.msg.split(), stdout=subprocess.PIPE, shell=False)
#			else:
#				try:
#					self.msg="adb -s device:"+self.device+" shell input keyevent "+str(self.dct[self.txt[i]])
#				except KeyError:
#					logger.error(self.txt[i]+' is unknown')				
#				self.p = subprocess.Popen(self.msg.split(), stdout=subprocess.PIPE, shell=False)
#			time.sleep(0.3)

#	def check (self):
#		self.msg="adb devices -l"
#		logger.info(self.msg)
#		self.p = subprocess.Popen(self.msg, stdout=subprocess.PIPE, shell=False)
#		(self.output, self.err) = self.p.communicate()
#		if self.ip not in self.output.decode():
#			self.connected=False
#			self.connect()
			
#	def monitor(self):
#		self.c=threading.Timer(600,self.monitor)
#		self.c.setDaemon(True)
#		self.c.start()
#		self.connect()

	def process(self,_input):
		try:
			if _input[0] == '1':
				self.key(_input[1])
			elif _input[0] == '2':
				threading.Thread(target=self.text,args=(_input[1],)).start()
		except IndexError:
			logger.error('wrong')

	def dproc(self,msg): #device msg processor
		print(msg.decode('ascii', errors='ignore'))
		
	def inform(self,caller):
		pass



dictadb=dict(
menu=b'OPEN9\x00\x00\x00\x00\x00\x00\x00\x17\x00\x00\x00^\x08\x00\x00\xb0\xaf\xba\xb1shell:input keyevent 1\x00',
home=b'OPEN7\x00\x00\x00\x00\x00\x00\x00\x17\x00\x00\x00`\x08\x00\x00\xb0\xaf\xba\xb1shell:input keyevent 3\x00',
back=b'OPEN5\x00\x00\x00\x00\x00\x00\x00\x17\x00\x00\x00a\x08\x00\x00\xb0\xaf\xba\xb1shell:input keyevent 4\x00',
up=b'OPENu\x00\x00\x00\x00\x00\x00\x00\x18\x00\x00\x00\x97\x08\x00\x00\xb0\xaf\xba\xb1shell:input keyevent 19\x00',
down=b'OPEN\x1b\x00\x00\x00\x00\x00\x00\x00\x18\x00\x00\x00\x8f\x08\x00\x00\xb0\xaf\xba\xb1shell:input keyevent 20\x00',
left=b'OPEN/\x00\x00\x00\x00\x00\x00\x00\x18\x00\x00\x00\x90\x08\x00\x00\xb0\xaf\xba\xb1shell:input keyevent 21\x00',
right=b'OPEN1\x00\x00\x00\x00\x00\x00\x00\x18\x00\x00\x00\x91\x08\x00\x00\xb0\xaf\xba\xb1shell:input keyevent 22\x00',
#center=b'OPENu\x00\x00\x00\x00\x00\x00\x00\x18\x00\x00\x00\x97\x08\x00\x00\xb0\xaf\xba\xb1shell:input keyevent 23\x00',
#volup=b'OPENu\x00\x00\x00\x00\x00\x00\x00\x18\x00\x00\x00\x97\x08\x00\x00\xb0\xaf\xba\xb1shell:input keyevent 24\x00',
#voldn=b'OPENu\x00\x00\x00\x00\x00\x00\x00\x18\x00\x00\x00\x97\x08\x00\x00\xb0\xaf\xba\xb1shell:input keyevent 25\x00',
clear=b'OPENA\x00\x00\x00\x00\x00\x00\x00\x18\x00\x00\x00\x97\x08\x00\x00\xb0\xaf\xba\xb1shell:input keyevent 28\x00',
#space=b'OPENu\x00\x00\x00\x00\x00\x00\x00\x18\x00\x00\x00\x97\x08\x00\x00\xb0\xaf\xba\xb1shell:input keyevent 62\x00',
enter=b'OPEN3\x00\x00\x00\x00\x00\x00\x00\x18\x00\x00\x00\x99\x08\x00\x00\xb0\xaf\xba\xb1shell:input keyevent 66\x00'
#delete=b'OPENu\x00\x00\x00\x00\x00\x00\x00\x18\x00\x00\x00\x97\x08\x00\x00\xb0\xaf\xba\xb1shell:input keyevent 67\x00',
)
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
