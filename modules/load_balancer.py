from config import BUFFER_SIZE
from modules.database import Database


class LoadBalancer:
    buffer = []
    workers = {}

    def ReceiveData(self, data_entry):
        LoadBalancer.buffer.append(data_entry)
        if len(LoadBalancer.buffer) < BUFFER_SIZE:
            return

        self.ProcessData()

    def ProcessData(self):
        for data_entry in LoadBalancer.buffer:
            pass  # Process data with worker here when it is implemented

    def GetWorker(self):
        pass
