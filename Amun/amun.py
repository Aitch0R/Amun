#import
import importlib
import infra.config as config

logger=importlib.import_module(config.mlogger)
logger.logger('mainLogger','Amun.log')
import logging
mLogger=logging.getLogger('Amun')
mLogger.info('Starting Amun')

logger.logger('commLogger','comm')

import threading
import sched
import subprocess
import time
import sys

mLogger.info('Importing modules')
gvar=importlib.import_module(config.gvar)
gvar.init()
resources=importlib.import_module(config.resources)
#import mymail
user=importlib.import_module(config.user)
protocols=importlib.import_module(config.protocols)
mLogger.info('Importing done')


#-------------------------------------------------------------------------------------------------


def run():
	'''start Amun'''
	print (resources.intro)
	user.scheduleMngr=user.scheduler()
	gvar.users.append(user.root())
	protocols.ra()

def help():
	'''print help text'''
	print(resources.help)

if __name__=="__main__":
	run()
