# import
import importlib
import logging
import threading
import infra.config as config

obj = importlib.import_module(config.obj).amunobj

logger = logging.getLogger('mainLogger')
logger.info('ir:OK')
# ---------------------------------------------------------------------

tvaeg = dict(const="57088,", volup='46155', voldn='45135', sourc='59415', mute='63240', ok='63750', exit='62730',
             power='58140', up='58650', down='46920', source='59415')


class ir(obj):
    def __init__(self, parent, info, preId, objid):
        obj.__init__(self, parent, info, preId, objid)
        self.sub = self.info['sub']
        self.agent = self.parent.agents[self.info['agent']]
        self.clientAddr = '4,' + str(self.objid)
        self.case = str(self.info['case'])
        if self.info['dct'] == 1:
            self._dict = tvaeg
        self.objstring = ',,ir,' + self.sub + ',' + str(self.objid) + ',' + self.name
        self.index = "5," + self.case + "," + self._dict['const']  # change index to case; 4 to 2
        self.cont = False

    def transmit(self, todo):
        self.todo = todo
        try:
            self.cmd = self.index + self._dict[self.todo]
            self.agent.objCmd(self.cmd)
        except KeyError:
            logger.error(self.todo + ' is unknown')

    def process(self, _input):
        self._input = _input
        if self._input[0] == 's':
            self.standBy(self._input[1])
        else:
            print(self._input[1])
            self.transmit(self._input[1])

    def inform(self, caller):  # override
        pass

    def powered(self, status):
        self._powered = status
        threading.Timer(10, self.transmit, args=('power',)).start()
