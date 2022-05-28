class Writer:
    def __init__(self, id, load_balancer):
        self.id = id
        self.active = False

    def SendData(self):
        pass

    def ManuallySendData(self):
        pass

    def CreateWorker(self):
        pass

    def DestroyWorkers(self):
        pass

    def ChangeWorkersStates(self):
        pass
