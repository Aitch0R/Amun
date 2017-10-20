import time

configs=dict(name='root', usrid=1,admin=True, port=1000,rooms=[0]) ##################change userid to userID, change 1 to 0, rooms to all
email='h.a.behery@gmail.com'
Pass='*********'
to=''

def cFunc(self):
	self.agent.objCmd(self.index+',s,0,500')
	print(self.index+',s,0,500)

def rule(self,msg):
	print(msg)
	self.input=msg.split(',')
	if(self.input[0]=='0' and self.input[1]=='2' and self.input[2]=='5' and self.input[4]==1):
		pass #threading.timer(rooms[0].objlists

def init(self,protocols):
	print('init')
	H=int(time.strftime('%H',time.localtime()))
#	m=int(time.strftime('%m',time.localtime()))
	if H>=6:
	      protocols.awake([0])
	self.scheduler.scheduler.add_job(protocols.asleep, trigger='interval', start_date='2017-09-29 00:00:00', args=[self.rooms], days=1)
	self.scheduler.scheduler.add_job(protocols.awake, trigger='interval', start_date='2017-09-29 6:30:00', args=[self.rooms], days=1)
	self.rooms[0].objlists[2][0].firstcontact=cFunc
#	self.scheduler.scheduler.add_job(self.scheduler.users[0].output, trigger='interval', start_date='2017-09-29 13:52:05', args=['stuff'], minutes=1)

