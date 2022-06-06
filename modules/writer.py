import os

from inquirer2 import prompt

from modules.load_balancer import LoadBalancer
from utils.color import *
from utils.object_parser import ObjectParser


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
        pass

    def __ManuallySendData(self):
        pass

    def __CreateWorker(self):
        pass

    @staticmethod
    def __DestroyWorkers():
        worker_names = ObjectParser.GetObjectNames(LoadBalancer.workers.values(), checkbox_data=True)
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
