import os

from inquirer2 import prompt

from modules.load_balancer import LoadBalancer
from utils.color import in_color, Color, print_in_color, cursor


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

    def __DestroyWorkers(self):
        pass

    def __ChangeWorkersStates(self):
        pass

    def __Close(self):
        pass

    @staticmethod
    def __ExecuteCleanMethod(method):
        os.system('cls' if os.name == 'nt' else 'clear')
        method()
