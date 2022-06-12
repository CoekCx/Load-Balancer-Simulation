import os
import threading
import time

from inquirer2 import prompt

from config import BUFFER_SIZE
from modules.worker import Worker
from utils.color import print_error, print_message


class LoadBalancer:
    buffer = []
    workers = {}

    @staticmethod
    def ReceiveData(data_entry):
        LoadBalancer.buffer.append(data_entry)
        if len(LoadBalancer.buffer) < BUFFER_SIZE:
            return

        os.system('cls' if os.name == 'nt' else 'clear')
        print_message('Data is being sent')
        new_thread = threading.Thread(target=LoadBalancer.__ProcessData)
        new_thread.start()
        return True

    @staticmethod
    def GetWorker():
        worker = LoadBalancer.__CheckForAvailableWorker()
        if not isinstance(worker, Worker):
            worker = LoadBalancer.__CheckForInactivateWorker()
            if isinstance(worker, Worker):
                worker.TurnOn()

        return worker

    @staticmethod
    def GetAllAvailableWorkers():
        available_workers = list(
            (worker for worker in LoadBalancer.workers.values() if worker.IsActive() and not worker.busy))
        if available_workers:
            return available_workers

        available_workers = list((worker for worker in LoadBalancer.workers.values() if not worker.IsActive()))
        if not available_workers:
            print_error('No available workers')
            return

        questions = [
            {
                'type': 'list',
                'name': 'user_input',
                'message': 'No available active workers, do you wish to show inactive workers?',
                'choices': ['Yes', 'No']
            }
        ]
        answers = prompt.prompt(questions)
        os.system('cls' if os.name == 'nt' else 'clear')
        if answers['user_input'] == 'Yes':
            return available_workers

    @staticmethod
    def GetAvailableWorker():
        available_worker = LoadBalancer.__CheckForAvailableWorker()
        if isinstance(available_worker, Worker):
            return available_worker

        available_worker = LoadBalancer.__CheckForInactivateWorker()
        if not isinstance(available_worker, Worker):
            print_error('No available workers')
            return

        questions = [
            {
                'type': 'list',
                'name': 'user_input',
                'message': f'No available active workers, do you wish to activate Worker {available_worker.id}?',
                'choices': ['Yes', 'No']
            }
        ]
        answers = prompt.prompt(questions)

        os.system('cls' if os.name == 'nt' else 'clear')
        if answers['user_input'] == 'Yes':
            available_worker.TurnOn()
            return available_worker

    @staticmethod
    def __CheckForAvailableWorker():
        for worker in LoadBalancer.workers.values():
            if worker.IsActive() and not worker.busy:
                return worker

    @staticmethod
    def __CheckForInactivateWorker():
        for worker in LoadBalancer.workers.values():
            if not worker.IsActive():
                return worker

    @staticmethod
    def __ProcessData():
        worker = LoadBalancer.__CheckForAvailableWorker()
        if not isinstance(worker, Worker):
            print_error('No available workers\nCancelled sending data and deleted last entry', clear_screen=True)
            LoadBalancer.buffer.pop()
            return

        while LoadBalancer.buffer:
            worker = LoadBalancer.GetWorker()
            if isinstance(worker, Worker):
                worker.ProcessWorkerAction('AddMeterConsumption', (LoadBalancer.buffer[len(LoadBalancer.buffer) - 1],))
                LoadBalancer.buffer.pop()
            time.sleep(0.25)
