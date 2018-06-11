import sys
import time
import socket
import threading
import importlib
import infra.config as config

gvar=importlib.import_module(config.gvar)
protocols=importlib.import_module(config.protocols)

btnMap=dict(_00000000111111110011101011000101='11', _00000000111111111011101001000101='12', _00000000111111111000001001111101='13', _00000000111111110000001011111101='14', _00000000111111110001101011100101='21', _00000000111111111001101001100101='22', _00000000111111111010001001011101='23', _00000000111111110010001011011101='24', _00000000111111110010101011010101='31', _00000000111111111010101001010101='32', _00000000111111111001001001101101='33', _00000000111111110001001011101101='34', _00000000111111110000101011110101='41', _00000000111111111000101001110101='42', _00000000111111111011001001001101='43', _00000000111111110011001011001101='44', _00000000111111110011100011000111='51', _00000000111111111011100001000111='52', _00000000111111110111100010000111='53', _00000000111111111111100000000111='54', _00000000111111110001100011100111='61', _00000000111111111001100001100111='62', _00000000111111110101100010100111='63', _00000000111111111101100000100111='64', _00000000111111110010100011010111='71', _00000000111111111010100001010111='72', _00000000111111110110100010010111='73', _00000000111111111110100000010111='74', _00000000111111110000100011110111='81', _00000000111111111000100001110111='82', _00000000111111110100100010110111='83', _00000000111111111100100000110111='84', _00000000111111110011000011001111='91', _00000000111111111011000001001111='92', _00000000111111110111000010001111='93', _00000000111111111111000000001111='94', _00000000111111110001000011101111='101', _00000000111111111001000001101111='102', _00000000111111110101000010101111='103', _00000000111111111101000000101111='104', _00000000111111110010000011011111='111', _00000000111111111010000001011111='112', _00000000111111110110000010011111='113', _00000000111111111110000000011111='114')

class ir_rcv(obj):
	def __init__(self,parent,info,objid,holder):
		self.parent=parent
		self.pin=4			#get pin from info
		self.sec=[]
		self.last=0
		self.ndinit()
		self.objstring='prelim'
		self.specInit()

	def process(self,inc):
		#String inc: incoming String

		try: #########################combine the signal comparison of the two dicts
			self.func['_'+btnMap['_'+self.io]]()
			print('io: 'self.io)
			print(btnMap['_'+self.io])
		except KeyError:
			try:
				self.func=self.mapofmaps['_'+btnMap['_'+self.io]]
				print ('rc mode: '+ self.func['name'])
			except KeyError:
#				print ('key not found') #################log as warning?
				pass

	def ndinit(self): #second part of the init
		self.protocols=dict(name='protocols', _14=protocols.shutdown)
		self.lights=dict(name='light', _24=self.l24, _34=self.l34, _44=self.l44, _54=self.l54, _61=self.l61, _62=self.l62)	
		self.tv=dict(name='tv', _22=self.t22, _31=self.t31, _32=self.t32, _33=self.t33, _42=self.t42, _44=self.t44, _51=self.t51, _52=self.t52, _53=self.t53, _54=self.t54, _62=self.t62, _73=self.t73, _64=self.t64, _72=self.t72, _74=self.t74, _82=self.t82, _84=self.t84, _94=self.t94)
		self.mapofmaps=dict(_101=self.lights, _111=self.tv, _114=self.protocols)
		self.func=self.lights
	
	def specInit(self):
		self.tv=self.parent.objlists[5][0]
		self.fire=self.parent.objlists[6][0]
		self.window1=self.parent.objlists[4][0]
		self.light1=self.parent.objlists[3][0]
	#------------------------------------------------------------------------------------
	#the big list #temporary

	def t22(self):
		self.fire.key('up')

	def t31(self):
		self.fire.key('left')

	def t32(self):
		self.fire.key('enter')

	def t33(self):
		self.fire.key('right')

	def t42(self):
		self.fire.key('down')

	def t51(self):
		self.fire.key('back')

	def t52(self):
		self.fire.key('home')

	def t53(self):
		self.fire.key('menu')

	def t54(self):
		pass #reserved for ch+

	def t63(self):
		self.tv.transmit('source')
	
	def t64(self):
                pass #reserved for ch-

	def t44(self):
		self.tv.tvpower()

	def t62(self):
		self.tv.transmit('up')

	def t73(self):
		self.tv.transmit('source')

	def t72(self):
		self.tv.transmit('ok')

	def t74(self):
		self.tv.transmit('volup')

	def t84(self):
		self.tv.transmit('voldn')

	def t82(self):
		self.tv.transmit('down')

	def t93(self):
		self.tv.transmit('exit')

	def t94(self):
		self.tv.transmit('mute')

	def _111(self):										#temporary on for all auto power sources
		self.parent.objlists[6][1].process('1')
		self.parent.objlists[6][2].process('1')
		self.parent.objlists[6][3].process('1')
		self.parent.objlists[6][5].process('1')

	def _112(self):										#temporary on for all auto power sources
		self.parent.objlists[6][1].process('0')
		self.parent.objlists[6][2].process('0')
		self.parent.objlists[6][3].process('0')
		self.parent.objlists[6][5].process('0')

	def _113(self):										#tv ps on
		self.parent.objlists[6][4].process('1')

	def _114(self):										#tv ps of
		self.parent.objlists[6][4].process('0')

	def l24(self):										#main light 100%
		self.light1=self.parent.objlists[3][0]
		self.light1.abslevel(100,0)

	def l54(self):										#main light 0%
		self.object=self.parent.objlists[2][0]
		self.light1.abslevel(0,0)

	def l34(self):										#main light step up
		self.val=self.light1.stufe+1
		self.light1.abslevel(int(self.val*self.val),0)

	def l44(self):										#main light step down
		self.val=self.light1.stufe-1
		self.light1.abslevel(int(self.val*self.val),0)

	def l61(self):										#right window blinds down
		self.val=self.window1.blnislvl+2
		self.window1.blnabslvl(self.val,0)	
	
	def l62(self):										#right window blinds up
		self.val=self.window1.blnislvl-2
		self.window1.blnabslvl(self.val,0)	
#----------------------------------------------------------------
	def inform(self,caller):
		pass
