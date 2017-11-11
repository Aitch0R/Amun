#usr1=dict(usrFile='users.aitch')
other=dict(name='other', usrid=2,admin=False, port=1002,rooms=[0])
users=[]#'users.aitch']

esp1=dict(agentId='0', port=151)
esp2=dict(agentId='1', port=160)
esp3=dict(agentId='2', port=170)
agents=[esp1,esp2,esp3]
#------------------------------------------------------------------------------------------------------
rooms=1

def roomlis(index):
	if (index==0):
		#regs
		_brightness= dict(typ='brightness', agent=0, c_index=0)
		#lights----------------
		light1= dict(typ='light',name='main light', cls=1,agent=0,agent_index='16',ps=3)
		light2= dict(typ='light',name='RGB Strip', cls=1,agent=0,agent_index='12',ps=3)
		light3= dict(typ='light',name='RGB Strip', cls=1,agent=0,agent_index='13',ps=3)
		light4= dict(typ='light',name='RGB Strip', cls=1,agent=0,agent_index='14',ps=3)
		#windows--------------
		window1= dict(typ='window',name='right window',agent=1,agent_index='12',ps=4)
		window2= dict(typ='window',name='left window',agent=1,agent_index='14',ps=4)
		#ir
		tv= dict(typ='ir',sub='tv', name="TV", agent=0, case="1",agent_index='5',dct=1,ps=5)
		#adb
		firestick= dict(typ='adb',device='montoya',ip='192.168.0.16',port=5555,dct=1,name='Fire Stick',ps=5)
		#powerS
		ps= dict(typ='powersupply',name='dummy',agent=2,agent_index='18')
		ps1= dict(typ='powersupply',name='powersupply1',agent=2,agent_index='A0')
		ps2= dict(typ='powersupply',name='powersupply2',agent=2,agent_index='2')
		ps3= dict(typ='powersupply',name='powersupply3',agent=2,agent_index='4')
		ps4= dict(typ='powersupply',name='powersupply4',agent=2,agent_index='5')
		ps5= dict(typ='powersupply',name='powersupply5',agent=2,agent_index='12')
		ps6= dict(typ='powersupply',name='powersupply6',agent=2,agent_index='13')
		ps7= dict(typ='powersupply',name='powersupply7',agent=2,agent_index='14')
		ps8= dict(typ='powersupply',name='powersupply8',agent=2,agent_index='16')
		#sensors
		ir_rcv= dict(typ='irsensor',name='ir reciever',ps=0)
		#thermostat
		thermostat=dict(typ='thermostat',name='heater',ps=3, agent=0,agent_index='2')
		_agents=[0]
		_objects = [ps,ps1,ps2,ps3,ps4,ps5,ps6,ps7,ps8,window1,window2,light1,light2,light3,light4,tv,firestick,ir_rcv,thermostat]
		_sensors=[_brightness]
		room= dict(name='myroom')
		
	#elif (index==1):
	#	
	#	light1= dict(typ='light',name='mainlight',cls=1,agent=0,agent_index=1)
	#	window1= dict(typ='window',name='main window',agent=0,agent_index='14')
	#	window2= dict(typ='window',name='side window',agent=0,agent_index='14')
	#	_brightness= dict(typ='brightness',agent=0,c_index=1)
	#	_agents=[0]
	#	_objects = [window1,window2,light1]
	#	_sensors=[_brightness]
	#	room=dict(name='kitchen',owner=1)'''

	else:
		_objects = []
		_sensors=[]
		room=dict(name='generic',owner=1)
	
	_room=dict(info=room,objects=_objects,sensors=_sensors)
	return _room	
#_____________________________________________________________________________________________________________
