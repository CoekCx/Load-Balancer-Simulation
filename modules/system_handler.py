import os
import re

from inquirer2 import prompt

from constants.regex import *
from factories.writer_factory import WriterFactory
from models.meter import Meter
from modules.database_analitics import DatabaseAnalytics
from modules.load_balancer import LoadBalancer
from modules.worker import Worker
from utils.color import print_message, print_error
from utils.object_parser import ObjectParser
from utils.validation import Validate


class SystemHandler:
    def __init__(self):
        self.writers = {}
        self.__functions = {
            'Write': self.__Write,
            'Manage writers': self.__ManageWriters,
            'Manage database': self.__ManageDatabase,
            'Create writers': self.__CreateWriters,
            'Destroy writers': self.__DestroyWriters,
            'Add meter': self.__AddMeter,
            'Modify meter': self.__ModifyMeter,
            'Delete meter': self.__DeleteMeters,
            'Reports': self.__ReportsPrompt,
            'City report': self.GetCityReport,
            'Meter report': self.GetMeterReport,
            'Quit': self.__Quit,
        }

    def Execute(self):
        self.ExecuteCleanMethod(self.__UserPrompt)

    def __UserPrompt(self):  # pragma: no cover
        choices = ['Write', 'Manage writers', 'Manage database', 'Reports', 'Quit']
        questions = [
            {
                'type': 'list',
                'name': 'user_input',
                'message': '|System>',
                'choices': choices,
            }
        ]
        answers = prompt.prompt(questions)

        self.ExecuteCleanMethod(self.__functions[answers['user_input']])

    def __Write(self):  # pragma: no cover
        if len(self.writers) == 0:
            print_error('No available writers', clear_screen=True)
            return

        writers = ['...']
        for writer in self.writers.values():
            writers.append(writer.__str__())

        questions = [
            {
                'type': 'list',
                'name': 'writer',
                'message': '|System>Writers>',
                'choices': writers,
                'default': 1
            }
        ]
        answers = prompt.prompt(questions)

        if answers['writer'] == '...':
            return

        writer = ObjectParser.GetClassObjectByName(self.writers.values(), answers['writer'])
        writer.active = True
        while writer.active:
            writer.Execute()

    def __ManageWriters(self):  # pragma: no cover
        choices = ['...', 'Create writers', 'Destroy writers']
        questions = [
            {
                'type': 'list',
                'name': 'user_input',
                'message': '|System>Writers>',
                'choices': choices,
                'default': 1
            }
        ]
        answers = prompt.prompt(questions)

        if answers['user_input'] == '...':
            return

        self.ExecuteCleanMethod(self.__functions[answers['user_input']])

    def __CreateWriters(self):  # pragma: no cover
        questions = [
            {
                'type': 'input',
                'name': 'amount_of_writers',
                'message': 'How many writers do you want to create',
                'validate': lambda x: True
                if Validate.ValidateIntValue(x, more_than=True, limit=0)
                else 'Invalid amount of writers to create'
            }
        ]
        answers = prompt.prompt(questions)

        WriterFactory.MakeWriter(int(answers['amount_of_writers']), self.writers.keys(), self.writers)

        self.writers = dict(sorted(self.writers.items()))
        print_message('Writers created', clear_screen=True)

    def __DestroyWriters(self):  # pragma: no cover
        if self.writers.__len__() == 0:
            print_error('There are no writers to destroy', clear_screen=True)
            return

        writer_names = ObjectParser.GetObjectNames(self.writers.values(), checkbox_data=True)
        questions = [
            {
                'type': 'checkbox',
                'name': 'writers_to_destroy',
                'message': 'Select workers to destroy',
                'choices': writer_names
            }
        ]
        answers = prompt.prompt(questions)
        writer_names_to_destroy = answers['writers_to_destroy']
        if not writer_names_to_destroy:
            return

        writers_to_destroy = []
        for writer in writer_names_to_destroy:
            writers_to_destroy.append(ObjectParser.GetClassObjectByName(self.writers.values(), writer))

        self.RemoveWritersFromDictionary(writers_to_destroy)
        print_message('Writers destroyed', clear_screen=True)

    def RemoveWritersFromDictionary(self, writers_to_destroy):
        removed_writer = False
        for writer in self.writers.values():
            if writer in writers_to_destroy:
                self.writers.__delitem__(writer.id)
                removed_writer = True
                break
        if removed_writer:
            self.RemoveWritersFromDictionary(writers_to_destroy)

    def __ManageDatabase(self):  # pragma: no cover
        choices = ['...', 'Add meter', 'Modify meter', 'Delete meter']

        questions = [
            {
                'type': 'list',
                'name': 'user_input',
                'message': "|System>Database>",
                'choices': choices,
            }
        ]
        answers = prompt.prompt(questions)
        if answers['user_input'] == '...':
            return

        self.ExecuteCleanMethod(self.__functions[answers['user_input']])

    def __AddMeter(self):  # pragma: no cover
        worker = LoadBalancer.GetAvailableWorker()
        if not isinstance(worker, Worker):
            return

        keys = worker.GetMetersKeys()
        questions = [
            {
                'type': 'input',
                'name': 'id',
                'message': 'Meter id',
                'validate': lambda x: True if Validate.ValidateExistenceOfIntValue(x, keys) else 'Invalid ID'
            },
            {
                'type': 'input',
                'name': 'first_name',
                'message': 'First name',
                'validate': lambda x: True if re.match(regex_word, x) else 'Invalid first name'
            },
            {
                'type': 'input',
                'name': 'last_name',
                'message': 'Last name',
                'validate': lambda x: True if re.match(regex_word, x) else 'Invalid last name'
            },
            {
                'type': 'input',
                'name': 'street_name',
                'message': 'Street name',
                'validate': lambda x: True if re.match(regex_words_and_numbers, x) else 'Invalid street name'
            },
            {
                'type': 'input',
                'name': 'street_number',
                'message': 'Street number',
                'validate': lambda x: True if Validate.ValidateIntValue(x, more_than=True,
                                                                        limit=0) else 'Invalid street number'
            },
            {
                'type': 'input',
                'name': 'zip_code',
                'message': 'Zip code',
                'validate': lambda x: True if Validate.ValidateIntValue(x) else 'Invalid zip code'
            },
            {
                'type': 'input',
                'name': 'city',
                'message': 'City',
                'validate': lambda x: True if re.match(regex_words_and_numbers, x) else 'Invalid city'
            }
        ]
        answers = prompt.prompt(questions)

        meter = Meter(int(answers['id']), answers['first_name'], answers['last_name'], answers['street_name'],
                      int(answers['street_number']), int(answers['zip_code']), answers['city'])
        worker.ProcessWorkerAction('AddMeter', (meter,))

    def __ModifyMeter(self):  # pragma: no cover
        worker = LoadBalancer.GetAvailableWorker()
        if not isinstance(worker, Worker):
            return

        meter = worker.SelectMeter('Edit meter')
        if not isinstance(meter, Meter):
            return

        os.system('cls' if os.name == 'nt' else 'clear')
        print(meter.__str__(show_info_color=True))

        questions = [
            {
                'type': 'input',
                'name': 'first_name',
                'message': 'First name',
                'validate': lambda x: True if re.match(regex_word, x) else 'Invalid first name',
                'default': meter.first_name
            },
            {
                'type': 'input',
                'name': 'last_name',
                'message': 'Last name',
                'validate': lambda x: True if re.match(regex_word, x) else 'Invalid last name',
                'default': meter.last_name
            },
            {
                'type': 'input',
                'name': 'street_name',
                'message': 'Street name',
                'validate': lambda x: True if re.match(regex_words_and_numbers, x) else 'Invalid street name',
                'default': meter.street_name
            },
            {
                'type': 'input',
                'name': 'street_number',
                'message': 'Street number',
                'validate': lambda x: True if Validate.ValidateIntValue(x) else 'Invalid street number',
                'default': str(meter.street_number)
            },
            {
                'type': 'input',
                'name': 'zip_code',
                'message': 'Zip code',
                'validate': lambda x: True if Validate.ValidateIntValue(x) else 'Invalid zip code',
                'default': str(meter.zip_code)
            },
            {
                'type': 'input',
                'name': 'city',
                'message': 'City',
                'validate': lambda x: True if re.match(regex_word, x) else 'Invalid city',
                'default': meter.city
            }
        ]
        answers = prompt.prompt(questions)

        self.ParseUpdatedMeter(meter, answers)
        worker.ProcessWorkerAction('UpdateMeter', (meter,))

    @staticmethod
    def ParseUpdatedMeter(meter, data):
        meter.first_name = data['first_name']
        meter.last_name = data['last_name']
        meter.street_name = data['street_name']
        meter.street_number = int(data['street_number'])
        meter.zip_code = int(data['zip_code'])
        meter.city = data['city']

    def __DeleteMeters(self):  # pragma: no cover
        worker = LoadBalancer.GetAvailableWorker()
        if not isinstance(worker, Worker):
            return

        meters = worker.GetAllMeters()
        meter_names = ObjectParser.GetObjectNames(meters, checkbox_data=True)
        questions = [
            {
                'type': 'checkbox',
                'name': 'meters_to_destroy',
                'message': 'Chose meters to destroy',
                'choices': meter_names
            }
        ]
        answers = prompt.prompt(questions)

        meters_to_destroy_names = answers['meters_to_destroy']
        meters_to_destroy = []
        for meter in meters_to_destroy_names:
            meters_to_destroy.append(ObjectParser.GetClassObjectByName(meters, meter))

        for meter in meters_to_destroy:
            worker.ProcessWorkerAction('DeleteMeter', (meter,))

    def __ReportsPrompt(self):  # pragma: no cover
        questions = [
            {
                'type': 'list',
                'name': 'user_input',
                'message': "|System>Reports>",
                'choices': ['...', 'City report', 'Meter report'],
                'default': 1
            }
        ]
        answers = prompt.prompt(questions)
        if answers['user_input'] == '...':
            return

        self.ExecuteCleanMethod(self.__functions[answers['user_input']])

    def GetCityReport(self):
        DatabaseAnalytics.ProvideCityPerMonthReport()

    def GetMeterReport(self):
        DatabaseAnalytics.ProvideMeterPerMonthReport()

    @staticmethod
    def __Quit():  # pragma: no cover
        exit(0)

    def ExecuteCleanMethod(self, method):
        os.system('cls' if os.name == 'nt' else 'clear')
        try:
            method()
        except KeyboardInterrupt or TypeError:
            self.Execute()
