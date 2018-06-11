#import
import importlib
import logging
import threading
import infra.config as config

obj=importlib.import_module(config.obj).amunobj
gvar=importlib.import_module(config.gvar)
protocols=importlib.import_module(config.protocols)

btnMap=dict(_00000000111111110011101011000101='11', _00000000111111111011101001000101='12', _00000000111111111000001001111101='13', _00000000111111110000001011111101='14', _00000000111111110001101011100101='21', _00000000111111111001101001100101='22', _00000000111111111010001001011101='23', _00000000111111110010001011011101='24', _00000000111111110010101011010101='31', _00000000111111111010101001010101='32', _00000000111111111001001001101101='33', _00000000111111110001001011101101='34', _00000000111111110000101011110101='41', _00000000111111111000101001110101='42', _00000000111111111011001001001101='43', _00000000111111110011001011001101='44', _00000000111111110011100011000111='51', _00000000111111111011100001000111='52', _00000000111111110111100010000111='53', _00000000111111111111100000000111='54', _00000000111111110001100011100111='61', _00000000111111111001100001100111='62', _00000000111111110101100010100111='63', _00000000111111111101100000100111='64', _00000000111111110010100011010111='71', _00000000111111111010100001010111='72', _00000000111111110110100010010111='73', _00000000111111111110100000010111='74', _00000000111111110000100011110111='81', _00000000111111111000100001110111='82', _00000000111111110100100010110111='83', _00000000111111111100100000110111='84', _00000000111111110011000011001111='91', _00000000111111111011000001001111='92', _00000000111111110111000010001111='93', _00000000111111111111000000001111='94', _00000000111111110001000011101111='101', _00000000111111111001000001101111='102', _00000000111111110101000010101111='103', _00000000111111111101000000101111='104', _00000000111111110010000011011111='111', _00000000111111111010000001011111='112', _00000000111111110110000010011111='113', _00000000111111111110000000011111='114')


logger = logging.getLogger('mainLogger')
logger.info(':OK') #######################################################change name
#---------------------------------------------------------------------
#relevants

class newObj(obj):
	def __init__(self,parent,info,objid):
		obj.__init__(self,parent,info,objid)
		#zero------------------------------------------------
		self.tStatus=0
		self.status=0
		#-----------------------------------------------------

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

	def compose(self, to):
		if to=='agentS':#setup
			msg=self.index+',s,'################################+'#something
		elif to=='agent':#cmd
			msg=self.index+',c,'###############################+'#something
		elif to=='client':
			msg=self.clientAddr+','+str(self.auto)+','######################+'#something
		return msg

	def aProcessor(self, incoming):
		'''String incoming: bin code'''
		try: #########################combine the signal comparison of the two dicts
			self.func['_'+btnMap[incoming]]()
			print(btnMap[incoming])
		except KeyError:
			try:
				self.func=self.mapofmaps['_'+btnMap[self.io]]
				print ('rc mode: '+ self.func['name'])
			except KeyError:
#                               print ('key not found') #################log as warning?
				pass
		self.informAll()
