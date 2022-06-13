import threading
import time
from random import randint

from inquirer2 import prompt

from config import LOWER_TIME_LIMIT, UPPER_TIME_LIMIT
from models.meter import Meter
from modules.database import Database
from utils.color import Color, in_color, print_error
from utils.object_parser import ObjectParser


class Worker:
    update_view = False

    def __init__(self, id, database: Database, active=False):
        self.id = id
        self.__database = database
        self.__active = active
        self.busy = False
        self.thread = None
        self.__actions = {
            'AddMeterConsumption': self.__ProcessMeterConsumption,
            'AddMeterConsumptions': self.__AddMeterConsumptions,
            'AddMeter': self.__ProcessMeterAdd,
            'UpdateMeter': self.__ProcessMeterUpdate,
            'DeleteMeter': self.__ProcessMeterDelete
        }

    def ProcessWorkerAction(self, action, args):
        self.thread = threading.Thread(target=self.__actions[action], args=args)
        self.thread.start()

    def __AddMeterConsumptions(self, meter_consumptions):
        for meter_consumption in meter_consumptions:
            self.__ProcessMeterConsumption(meter_consumption)

    def __ProcessMeterConsumption(self, datapoint):
        self.StateChange(is_busy=True, reload_view=True)
        time.sleep(randint(LOWER_TIME_LIMIT, UPPER_TIME_LIMIT))
        Database.AddMeterConsumption(datapoint)
        self.StateChange(is_busy=False, reload_view=True)

    def __ProcessMeterAdd(self, meter):
        self.StateChange(is_busy=True, reload_view=True)
        time.sleep(randint(LOWER_TIME_LIMIT, UPPER_TIME_LIMIT))
        Database.AddMeter(meter)
        self.StateChange(is_busy=False, reload_view=True)

    def __ProcessMeterUpdate(self, meter):
        self.StateChange(is_busy=True, reload_view=True)
        time.sleep(randint(LOWER_TIME_LIMIT, UPPER_TIME_LIMIT))
        Database.UpdateMeter(meter)
        self.StateChange(is_busy=False, reload_view=True)

    def __ProcessMeterDelete(self, meter):
        self.StateChange(is_busy=True, reload_view=True)
        time.sleep(randint(LOWER_TIME_LIMIT, UPPER_TIME_LIMIT))
        Database.DeleteMeter(meter)
        self.StateChange(is_busy=False, reload_view=True)

    @staticmethod
    def GetMetersKeys():
        return Database.GetMeterKeys()

    @staticmethod
    def GetAllMeters():
        meter_data = Database.GetAllMeters()
        meters = []
        for meter in meter_data:
            meters.append(Meter(meter[0], meter[1], meter[2], meter[3], meter[4], meter[5], meter[6]))

        return meters

    @staticmethod
    def SelectCity(message=''):
        results = Database.GetAllCities()
        if not results:
            print_error('There is no city data')
            return

        cities = []
        for result in results:
            cities.append(result[0])
        cities.insert(0, '...')
        questions = [
            {
                'type': 'list',
                'name': 'city',
                'message': message,
                'choices': cities,
                'default': 1
            }
        ]
        answers = prompt.prompt(questions)

        city = answers['city']
        if city != '...':
            return city

    def SelectMeter(self, message='Select meter', show_meter_info=False):
        meters = self.GetAllMeters()
        if not meters:
            print_error('There are no existing meters')
            return

        meter_names = ObjectParser.GetObjectNames(meters)
        meter_names.insert(0, '...')
        questions = [
            {
                'type': 'list',
                'name': 'meter',
                'message': message,
                'choices': meter_names,
                'default': 1
            }
        ]
        answers = prompt.prompt(questions)

        meter = ObjectParser.GetClassObjectByName(meters, answers['meter'])
        if meter != '...':
            return meter

    def IsActive(self):
        return self.__active

    def SwitchState(self):
        self.__active = not self.IsActive()

    def StateChange(self, is_busy, reload_view=False):
        self.busy = is_busy
        if reload_view:
            Worker.update_view = True

    def TurnOn(self):
        self.__active = True

    def TurnOff(self):
        self.__active = False

    def __eq__(self, other):
        if not isinstance(other, Worker):
            return False
        if self.id == other.id:
            return True
        return False

    def __str__(self, show_color=False, show_activity=False, show_availability=False):
        if self.IsActive():
            active = in_color('Active\t', Color.GREEN)
        else:
            active = in_color('InActive', Color.RED)

        if self.busy:
            busy = in_color('Busy', Color.RED)
        else:
            busy = in_color('Free', Color.GREEN)

        if show_color:
            name = f'{in_color(f"Worker {self.id}", Color.YELLOW)}'
        else:
            name = f'Worker {self.id}'

        if show_activity:
            name += f'\t{active}'
        if show_availability:
            name += f'\t{busy}'

        return name
