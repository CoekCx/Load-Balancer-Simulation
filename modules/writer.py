from inquirer2 import prompt

from constants import time
from models.meter import Meter
from models.meter_consumption import DataPoint
from modules.load_balancer import LoadBalancer
from modules.worker import Worker
from utils.color import *
from utils.object_parser import ObjectParser
from utils.validation import Validate


class Writer:
    def __init__(self, id):
        self.id = id
        self.active = False
        self.__functions = {
            'Show worker statuses': self.__ShowWorkerStatuses,
            'Send data using Load Balancer': self.__SendData,
            'Send data manually': self.__ManuallySendData,
            'Create worker': self.__CreateWorker,
            'Destroy workers': self.__DestroyWorkers,
            'Manage workers': self.__ChangeWorkersStates,
            'Close writer': self.__Close
        }

    def Execute(self):
        self.active = True
        self.__ExecuteCleanMethod(self.__UserPrompt)

    def __UserPrompt(self):
        choices = ['Show worker statuses', 'Send data using Load Balancer', 'Send data manually', 'Create worker',
                   'Destroy workers', 'Manage workers', 'Close writer']
        questions = [
            {
                'type': 'list',
                'name': 'user_input',
                'message': f"|System>>Writer {self.id}>",
                'choices': choices,
            }
        ]

        answers = prompt.prompt(questions)
        self.__ExecuteCleanMethod(self.__functions[answers['user_input']])

    @staticmethod
    def __ShowWorkerStatuses():
        if len(LoadBalancer.workers) == 0:
            print_in_color('No workers to show', Color.RED)
        for worker in LoadBalancer.workers.values():
            print(worker)
        cursor()
        input()

    def __SendData(self):
        worker = LoadBalancer.GetAvailableWorker()
        if not isinstance(worker, Worker):
            return

        new_data_entry = self.__InputDataEntry(worker)
        if not isinstance(new_data_entry, DataPoint):
            return

        if LoadBalancer.ReceiveData(data_entry=new_data_entry):
            self.__ShowWorkerStatuses()
        else:
            print_message(f'Sent: {new_data_entry}', clear_screen=True)

    def __ManuallySendData(self):
        available_workers = LoadBalancer.GetAllAvailableWorkers()
        if not available_workers:
            return

        worker_names = ObjectParser.GetObjectNames(available_workers)
        worker_names.insert(0, '...')
        message = 'Use worker' if available_workers[0].IsActive() else 'Worker to activate'
        questions = [
            {
                'type': 'list',
                'name': 'worker',
                'message': message,
                'choices': worker_names,
                'default': 1
            }
        ]
        answers = prompt.prompt(questions)
        os.system('cls' if os.name == 'nt' else 'clear')
        if answers['worker'] == '...':
            return

        worker = ObjectParser.GetClassObjectByName(available_workers, answers['worker'])
        if not worker.IsActive():
            worker.TurnOn()
        new_data_entry = self.__InputDataEntry(worker)
        if not isinstance(new_data_entry, DataPoint):
            return

        worker.ProcessWorkerAction('AddMeterConsumption', (new_data_entry,))
        print_message(f'Sent: {new_data_entry}', clear_screen=True)

    @staticmethod
    def __InputDataEntry(worker):
        meter = worker.SelectMeter()
        if not isinstance(meter, Meter):
            return

        questions = [
            {
                'type': 'input',
                'name': 'value',
                'message': 'Data point value',
                'validate': lambda x: True if Validate.ValidateIntValue(x, more_than=True,
                                                                        limit=0) else 'Invalid data point value'
            },
            {
                'type': 'list',
                'name': 'month',
                'message': 'Data point month',
                'choices': time.months
            }
        ]
        answers = prompt.prompt(questions)
        new_data_entry = DataPoint(meter.id, int(answers['value']), answers['month'])
        return new_data_entry

    def __CreateWorker(self):
        pass

    def __DestroyWorkers(self):
        pass

    @staticmethod
    def __ChangeWorkersStates():
        worker_names = ObjectParser.GetObjectNames(LoadBalancer.workers.values(), checkbox_data=True)
        questions = [
            {
                'type': 'checkbox',
                'name': 'statuses',
                'message': 'Manage workers:',
                'choices': worker_names
            }
        ]
        answers = prompt.prompt(questions)

        workers = []
        for worker in answers['statuses']:
            workers.append(ObjectParser.GetClassObjectByName(LoadBalancer.workers.values(), worker))

        Writer.__UpdateWorkerStates(workers)

    @staticmethod
    def __UpdateWorkerStates(statuses):
        for worker in LoadBalancer.workers.values():
            if worker in statuses:
                worker.SwitchState()

    def __Close(self):
        pass

    @staticmethod
    def __ExecuteCleanMethod(method):
        os.system('cls' if os.name == 'nt' else 'clear')
        method()
