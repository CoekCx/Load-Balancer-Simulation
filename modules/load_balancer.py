from config import BUFFER_SIZE
from modules.database import Database


class LoadBalancer:
    buffer = []
    workers = {}

    @staticmethod
    def GetAvailableWorker():
        # TODO: Implement
        #  Implement
        pass

    @staticmethod
    def GetAllAvailableWorkers():
        # TODO: Implement
        #  Implement
        pass

    @staticmethod
    def ReceiveData(data_entry):
        LoadBalancer.buffer.append(data_entry)
        if len(LoadBalancer.buffer) < BUFFER_SIZE:
            return

        LoadBalancer.ProcessData()

    @staticmethod
    def ProcessData():
        for data_entry in LoadBalancer.buffer:
            pass  # Process data with worker here when it is implemented
