from modules.load_balancer import LoadBalancer
from utils.color import print_in_color, Color, cursor


class Writer:
    def __init__(self, id, load_balancer):
        self.id = id
        self.active = False

    def ShowWorkerStatuses(self):
        if len(LoadBalancer.workers) == 0:
            print_in_color('No workers to show', Color.RED)
        for worker in LoadBalancer.workers.values():
            print(worker)
        cursor()

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
