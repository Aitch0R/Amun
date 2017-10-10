import sys
import time
import socket
import threading
import RPi.GPIO as GPIO

#global last
#global d
#raw=[]
#sec=[]
#last=0

connected=False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
btnMap=dict(_00000000111111110011101011000101='1,1', _00000000111111111011101001000101='1,2', _00000000111111111000001001111101='1,3', _00000000111111110000001011111101='1,4', _00000000111111110001101011100101='2,1', _00000000111111111001101001100101='2,2', _00000000111111111010001001011101='2,3', _00000000111111110010001011011101='2,4', _00000000111111110010101011010101='3,1', _00000000111111111010101001010101='3,2', _00000000111111111001001001101101='3,3', _00000000111111110001001011101101='3,4', _00000000111111110000101011110101='4,1', _00000000111111111000101001110101='4,2', _00000000111111111011001001001101='4,3', _00000000111111110011001011001101='4,4', _00000000111111110011100011000111='5,1', _00000000111111111011100001000111='5,2', _00000000111111110111100010000111='5,3', _00000000111111111111100000000111='5,4', _00000000111111110001100011100111='6,1', _00000000111111111001100001100111='6,2', _00000000111111110101100010100111='6,3', _00000000111111111101100000100111='6,4', _00000000111111110010100011010111='7,1', _00000000111111111010100001010111='7,2', _00000000111111110110100010010111='7,3', _00000000111111111110100000010111='7,4', _00000000111111110000100011110111='8,1', _00000000111111111000100001110111='8,2', _00000000111111110100100010110111='8,3', _00000000111111111100100000110111='8,4', _00000000111111110011000011001111='9,1', _00000000111111111011000001001111='9,2', _00000000111111110111000010001111='9,3', _00000000111111111111000000001111='9,4', _00000000111111110001000011101111='10,1', _00000000111111111001000001101111='10,2', _00000000111111110101000010101111='10,3', _00000000111111111101000000101111='10,4', _00000000111111110010000011011111='11,1', _00000000111111111010000001011111='11,2', _00000000111111110110000010011111='11,3', _00000000111111111110000000011111='11,4')

class ir_rcv(object):
	def __init__(self,parent,info,objid,holder):
		self.pin=17
		self.raw=[]
		self.sec=[]
		self.last=0
		GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD  
		GPIO.setup(self.pin, GPIO.IN,pull_up_down=GPIO.PUD_UP)
		self.objstring='prelim'
		print ('listening')
		GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=self.catch)

	def catch(self, channel):
		self.current=int(time.time()*1000000)
		self.d=self.current-self.last
		self.last=self.current
		self.le=0
		self.raw.append(self.d)
		if self.d<10000 and self.le < 67:
			self.sec.append(self.d)
			self.le=self.le+1
		else:
			self.binTrans(self.sec)
			self.sec=[]
			self.le=0

	def binTrans(self, sec):
		self.l=len(sec)
		self.i=3
		self.io='_'
		print (self.raw)
		self.raw = []
		print (self.sec)
		while self.i < self.l:
			if self.sec[self.i]<1000:
				self.io=self.io+'0'
			elif self.sec[self.i]>1000:
				self.io=self.io+'1'
			self.i=self.i+2
		print (self.l)
		try:
			print (self.io)
			print (btnMap[self.io])
	#		send(btnMap[io])
		except KeyError:
			pass
		#match(io)	
	'''while True:
                check()
                time.sleep(1000)
if __name__=='__main__':
	pass'''
'''
def send(msg):
	msg=msg+'\n'
	try:
		s.sendall(msg.encode())
	except socket.error:
		connected=False
	
def run():
	GPIO.add_event_detect(pin, GPIO.BOTH, callback=catch)
	
def check():
	while connected or keepAlive:
		pass
		
try:
	s.connect(('192.168.0.10', port))
	connected=True
except socket.error:
        pass

GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD  
GPIO.setup(pin, GPIO.IN,pull_up_down=GPIO.PUD_UP)
run()
print ('listening')

try:
	while True:
		check()
		time.sleep(1000)
	#threadcheck hreading.Thread(target=check)
	#threadcheck.setDaemon(False)
	#threadcheck.start()
except KeyboardInterrupt:
	GPIO.cleanup
	exit()


GPIO.cleanup()
'''

