#import
import importlib
import logging
import threading
import time
#import RPi.GPIO as GPIO
import infra.config as config

gvar=importlib.import_module(config.gvar)
structure=importlib.import_module(config.structure)
agent=importlib.import_module(config.agent).agent
user=importlib.import_module(config.user)
server=importlib.import_module(config.wcom).server
room=importlib.import_module(config.room).room
logger = logging.getLogger('mainLogger')
#-------------------------------------------------------------------------------
b_ra=False
rooms=gvar.rooms
users=gvar.users
agents=gvar.agents

def ra():
	#BUILD
	#agents
	for gnt in structure.agents:
		agents.append(agent(gnt))
	#room construct
	for index in range(0,structure.rooms):
		_room=structure.roomlis(index)
		rooms.append(room(_room,index,agents))
	config.roomlist=rooms
	#users
	for usr in structure.users:
		users.append(user.user(usr))
#	threading.Timer(10,users[0].raOk).start()
	time.sleep(10)
	users[0].raOk()
	logger.info('----Amun Ready----')

def awake(roomsId):
	for id in roomsId:
		room=rooms[id]
		room.objlists[2][6].power(1)
		room.objlists[2][0].power(1)
		room.objlists[2][0].status=1
		room.objlists[2][0].informAttached()
		time.sleep(2)
		room.objlists[3][0].standBy('1')
		room.objlists[4][0].standBy('1')

def asleep(roomsId): ####################fix
	for id in roomsId:
		room=rooms[id]
		room.objlists[2][6].power(1)
		room.objlists[2][0].informAttached()
###             turn heater off
		time.sleep(6)
		lists=[4,5]
		for id in lists:
			for obj in room.objlists[id]:
				obj.standBy('0')

def out(roomsId):
	for id in roomsId:
		room=rooms[id]
		# turn off all heaters and wait 6 seconds after each
		for thermostat in room.objlists[8]:
			thermostat.setState('0','t')
			time.sleep(6)
		lists=[3,4,5,6,7]
		for id in lists:
			for obj in room.objlists[id]:
				obj.standBy('0')

def suspend():
	for obj in rooms[0].objlists[2]:
		obj.power(0)

def shutdown():
	for room in gvar.rooms:
		print('shutting')
		room.shutdown(False)
	for agent in gvar.agents:
		agent.shutdown()
	for user in gvar.users:
		user.shutdown()
#	GPIO.cleanup()
	threading.Timer(1,exit).start()
#-------------------------------------------------------------------------------------
logger.info('Protocols:OK')
