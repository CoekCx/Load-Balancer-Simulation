import os

import constants.time
from models.meter import Meter
from modules.database import Database
from modules.load_balancer import LoadBalancer
from modules.worker import Worker
from utils.color import in_color, Color, cursor


class DatabaseAnalytics:

    @staticmethod
    def ProvideCityPerMonthReport():
        worker = LoadBalancer.GetAvailableWorker()
        if not isinstance(worker, Worker):
            return

        city = worker.SelectCity()
        if not city:
            return

        meter_consumptions = Database.GetMeterConsumptionByCity(city)
        DatabaseAnalytics.GenerateEntityPerMonthReport(in_color(city, Color.GREEN, True), meter_consumptions)

    @staticmethod
    def ProvideMeterPerMonthReport():
        worker = LoadBalancer.GetAvailableWorker()
        if not isinstance(worker, Worker):
            return

        meter = worker.SelectMeter('Show report for meter')
        if not isinstance(meter, Meter):
            return

        meter_consumptions = Database.GetMeterConsumptionByMeter(meter.id)
        DatabaseAnalytics.GenerateEntityPerMonthReport(meter, meter_consumptions)

    @staticmethod
    def GenerateEntityPerMonthReport(entity, meter_consumptions):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(entity)
        for month in constants.time.months:
            datapoint_exists_month = False
            for datapoint in meter_consumptions:
                if datapoint.month == month:
                    datapoint_exists_month = True
                    break
            if datapoint_exists_month:
                print(f'\t{in_color(month, Color.GREEN, True)}')
            for datapoint in meter_consumptions:
                if datapoint.month == month:
                    print(f'\t\t{datapoint}')
        cursor()
        input()
