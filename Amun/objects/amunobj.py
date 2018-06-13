import logging


class amunobj(object):
    def __init__(self, parent, info, preId, objid):
        self.parent = parent
        self.info = info
        self.preId = str(preId)
        self.preStr = self.info['preStr']
        self.name = self.info['name']
        self.objid = objid
        self.auto = 0
        self.isPowered = False
        self.isConnected = False
        self.isActive = 0
        self.agent = self.parent.agents[self.info['agent']]
        self.index = str(self.info['agent_index'])
        self.agent.insert(self, self.index)
        self.clientAddr = self.preId + ',' + str(self.objid)
        self.objstring = ',,' + self.preStr + ',' + str(self.objid) + ',' + self.name
        self.powerS = self.parent.objlists[2][self.info['ps']]
        self._standby = False
        self.powerS.enlist(self)

    def compose(self, to):  ###specific
        if to == 'client':
            msg = self.clientAddr + ',' + str(isActive)
        return msg

    def status(self):  # get status from agent by sending setup cmd
        self.agent.objCmd(self.compose('agentS'))

    def powered(self, status):
        self.isPowered = status
        self.chkActive()

    def standBy(self, status):
        if status in ['0', '1']:
            self._standby = status
            self.powerS.check()

    def inform(self, caller):  # inform caller
        caller.inform(str(self.parent.id) + ',' + self.compose('client'))

    # inform all users of the current status
    def informAll(self, msg='dummy'):  # dummy place holder for parent objects
        print(self.compose('client'))
        self.parent.informAll(self.compose('client'))

    def display(self, msg):
        self.parent.lcdDisplay(self.name, msg, 5)

    def connected(self, state):
        self.isConnected = state
        self.chkActive()

    def chkActive(self):
        if self.isConnected and self.isPowered:
            self.temp = 1
        else:
            self.temp = 0
        if self.isActive is not self.temp:
            self.isActive = self.temp
            self.parent.informAll(self.compose('client'))

    def process(self, _input):
        pass

    def aProcessor(self, _input):
        pass

    def first_contact(self):
        pass