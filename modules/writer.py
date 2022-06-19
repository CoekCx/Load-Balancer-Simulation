import threading
import time

from inquirer2 import prompt

import constants.time
from factories.worker_factory import WorkerFactory
from models.meter import Meter
from models.meter_consumption import DataPoint
from modules.load_balancer import LoadBalancer
from modules.worker import Worker
from utils.color import *
from utils.object_parser import ObjectParser
from utils.validation import Validate


class Writer:
    stop_showing_workers = False

    def __init__(self, id):
        self.id = id
        self.active = False
        self.__functions = {
            'Show worker statuses': self.ShowWorkerStatuses,
            'Send data using Load Balancer': self.SendData,
            'Send data manually': self.__ManuallySendData,
            'Create worker': self.__CreateWorker,
            'Destroy workers': self.__DestroyWorkers,
            'Manage workers': self.__ChangeWorkersStates,
            'Close writer': self.Close
        }

    def Execute(self):
        self.active = True
        self.ExecuteCleanMethod(self.__UserPrompt)

    def __UserPrompt(self):  # pragma: no cover
        choices = ['Show worker statuses', 'Send data using Load Balancer', 'Send data manually', 'Create worker',
                   'Destroy workers', 'Manage workers', 'Close writer']
        questions = [
            {
                'type': 'list',
                'name': 'user_input',
                'message': f"|System>Writer {self.id}>",
                'choices': choices,
            }
        ]
        answers = prompt.prompt(questions)

        self.ExecuteCleanMethod(self.__functions[answers['user_input']])

    def ShowWorkerStatuses(self):
        new_thread = threading.Thread(target=self.ViewWorkers)
        Worker.update_view = True
        new_thread.start()
        time.sleep(0.1)
        input()
        Writer.stop_showing_workers = True

    def ViewWorkers(self):
        Writer.stop_showing_workers = False
        while not Writer.stop_showing_workers:
            if Worker.update_view:
                os.system('cls' if os.name == 'nt' else 'clear')
                if len(LoadBalancer.workers) == 0:
                    print_in_color('No workers to show', Color.RED)

                for worker in LoadBalancer.workers.values():
                    print(worker.__str__(show_color=True, show_activity=True, show_availability=True))

                cursor()
                time.sleep(0.1)
                Worker.update_view = False
            time.sleep(0.2)

    def SendData(self):
        worker = LoadBalancer.GetAvailableWorker()
        if not isinstance(worker, Worker):
            return

        new_data_entry = self.InputDataEntry(worker)
        if not isinstance(new_data_entry, DataPoint):
            return

        if LoadBalancer.ReceiveData(data_entry=new_data_entry):
            self.ShowWorkerStatuses()
        else:
            print_message(f'Sent: {new_data_entry}', clear_screen=True)

    def __ManuallySendData(self):  # pragma: no cover
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
        new_data_entry = self.InputDataEntry(worker)
        if not isinstance(new_data_entry, DataPoint):
            return

        worker.ProcessWorkerAction('AddMeterConsumption', (new_data_entry,))
        print_message(f'Sent: {new_data_entry}', clear_screen=True)

    @staticmethod
    def InputDataEntry(worker):  # pragma: no cover
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
                'choices': constants.time.months
            }
        ]
        answers = prompt.prompt(questions)
        new_data_entry = DataPoint(meter.id, int(answers['value']), answers['month'])
        return new_data_entry

    @staticmethod
    def __CreateWorker():  # pragma: no cover
        questions = [
            {
                'type': 'input',
                'name': 'worker_amount',
                'message': 'How many workers do you want to create',
                'validate': lambda x: True
                if Validate.ValidateIntValue(x, more_than=True, limit=0)
                else 'Invalid amount of workers to create'
            }
        ]
        answers = prompt.prompt(questions)
        WorkerFactory.MakeWorker(int(answers['worker_amount']))
        LoadBalancer.workers = dict(sorted(LoadBalancer.workers.items()))
        print_message('Workers created', clear_screen=True)

    def __DestroyWorkers(self):  # pragma: no cover
        worker_names = ObjectParser.GetObjectNames(LoadBalancer.workers.values(), checkbox_data=True)
        if not worker_names:
            return

        questions = [
            {
                'type': 'checkbox',
                'name': 'workers_to_destroy',
                'message': 'Select workers to destroy',
                'choices': worker_names,
            }
        ]
        answers = prompt.prompt(questions)

        for worker in answers['workers_to_destroy']:
            worker = ObjectParser.GetClassObjectByName(LoadBalancer.workers.values(), worker)
            LoadBalancer.workers.pop(worker.id)

    def __ChangeWorkersStates(self):  # pragma: no cover
        worker_names = ObjectParser.GetObjectNames(LoadBalancer.workers.values(), checkbox_data=True)
        if not worker_names:
            return

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

        self.UpdateWorkerStates(workers)

    def UpdateWorkerStates(self, statuses):
        for worker in LoadBalancer.workers.values():
            if worker in statuses:
                worker.SwitchState()

    def Close(self):
        self.active = False

    def ExecuteCleanMethod(self, method):
        os.system('cls' if os.name == 'nt' else 'clear')
        try:
            method()
        except KeyboardInterrupt or TypeError:
            self.Execute()

    def __str__(self, show_info_in_color=False):  # pragma: no cover
        if show_info_in_color:
            return in_color(f"Writer {self.id}", Color.BLUE)
        else:
            return f'Writer {self.id}'
