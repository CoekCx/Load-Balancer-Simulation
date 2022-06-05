class Worker:
    def __init__(self, id, database, active=False):
        self.id = id
        self.__database = database
        self.__active = active
        self.busy = False

    @staticmethod
    def SelectMeter():
        # TODO: Implement
        #  Implement
        pass

    def AddMeterConsumptions(self, meter_consumptions):
        pass

    def AddMeter(self, meter):
        pass

    def UpdateMeter(self, meter):
        pass

    def DeleteMeter(self, meter):
        pass

    def GetAllMeters(self):
        pass

    def IsActive(self):
        return self.__active

    def SwitchState(self):
        self.__active = not self.IsActive()

    def TurnOn(self):
        self.__active = True

    def TurnOff(self):
        self.__active = False
