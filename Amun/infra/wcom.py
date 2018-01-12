import logging
import socket
import threading

logger = logging.getLogger('mainLogger')
comm = logging.getLogger('commLogger')

class server(object):
	def __init__(self,parent,info):
		self.parent=parent
		self.caller=2
		self.info=info
		#self.name=self.info['name']
		self.ip ='192.168.0.10'
		self.port=self.info['port']
		self.isConnected=False
		self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.logger_id='client:'+ str(self.port)+' '
		logger.info(self.logger_id)
		self.s.bind((self.ip,self.port))	
		self.up()
				
	def up(self):
		self.thread = threading.Thread(target=self.rcvcom)
		self.thread.setDaemon(True)
		self.thread.start()

	def rcvcom(self):
		self.s.listen(1)
		while True:
			self.conn, self.addr = self.s.accept()
			self.connected(True)
			self.rfile = self.conn.makefile()
			while True:
				try:
					self.data = self.rfile.readline().strip()
					if not self.data:
						break;
#					comm.debug('from:'+str(self.port)+' msg:'+self.data)
					self.incom=threading.Thread(target=self.parent.process, args=(self.caller,self.data.split(','),))
					self.tempLog(self.data.split(','))
					self.incom.start()
				except ConnectionResetError:
					break		
			self.connected(False)
			logger.warning(self.logger_id+'connection lost')

	def send(self,msg):
		self.msg=msg+'\n'
		try:
			comm.debug('to:'+str(self.port)+' msg:'+msg)
			self.conn.sendall(self.msg.encode())
		except AttributeError:
			self.connected(False)
		except BrokenPipeError:
			self.connected(False)

	def connected(self, state):
		self.isConnected=state
		self.parent.connected(state)
		logger.info(self.logger_id+'is connected: '+str(self.isConnected))
	
	def shutdown(self):
		self.s.close()

	def statusUpdate(self,caller): ###############create class for esp and re write
		pass

	def tempLog(self, inp):
		if inp[0]=='0' and inp[1]=='0': #################avoid logging brightness till reducing the range to 100
			pass
		else:
			comm.debug('from:'+str(self.port)+' msg:'+self.data)

class port(object):
	def __init__(self,parent,info):
		self.parent=parent
		self.caller=2
		self.info=info
		#self.name=self.info['name']
		self.ip =self.info['ip']
		self.port=self.info['port']
		self.isConnected=False
		self.s=None
		self.logger_id='port:'+ str(self.port)+' '
		logger.info(self.logger_id)
			
	def up(self): ###############################insert retry if powered at all
		try:
			print('trying to connect')
			self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.s.connect((self.ip,self.port))
			self.thread1 = threading.Thread(target=self.rcvcom)
			self.thread1.setDaemon(True)
			self.thread1.start()
			self.connected(True)
		except OSError:
			print('connect-OSE')
			self.connected(False)
			self.shutdown()
		except ValueError:
			pass

	def send(self,msg):
		print('in send')
		if not self.isConnected:	
			self.up()
		try:
			self.s.send(msg)
		except AttributeError:
			pass
		except OSError:
			print('send-OSE')
			self.connected(False)
			self.shutdown()
		except BrokenPipeError:
			print('send-BPE')
			self.connected(False)
		except ConnectionResetError:
			print('send-CRE')
			self.connected(False)

	def rcvcom(self):
		while self.isConnected:
			try:
				self.incom = self.s.recv(4096)
				if not self.incom:
					break; 
				self.parent.dproc(self.incom)
				self.rfile=None		
			except ConnectionResetError:	
				self.connected(False)
				break;

	def connected(self, state):
		self.isConnected=state
		self.parent.connected(state)
		logger.info(self.logger_id+'is connected: '+str(self.isConnected))
		if state==False:
			pass
#			self.up()

	def shutdown(self):
		try:
			self.s.shutdown(socket.SHUT_RDWR)
		except OSError:
			print('in shut-OSE')
		self.s.close()
