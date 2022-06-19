import sys

sys.path.append("C:/Users/Milos/Documents/FAKULTET/3 godina/6_semestar/RES/Python/"
                "python-project-main-final/python-project-main")

import unittest
from unittest.mock import patch
from modules.database_analitics import DatabaseAnalytics
from modules.worker import Worker
from models.meter import Meter
from models.meter_consumption import DataPoint


class TestDatabaseAnalytics(unittest.TestCase):

    def setUp(self):
        self.meter = Meter("1", "Nikola", "Tesla", "Cara Lazara", "13", "10100", "Beograd")
        self.meter_consumptions = [DataPoint('1', 20, 'January'), DataPoint('2', 28, 'February')]

    @patch("modules.database.Database.GetMeterConsumptionByMeter")
    @patch("modules.database_analitics.DatabaseAnalytics.GenerateEntityPerMonthReport")
    def test_ProvideCityPerMonthReport(self, arg, arg1):
        with patch("modules.load_balancer.LoadBalancer.GetAvailableWorker", return_value=None):
            self.assertEqual(DatabaseAnalytics.ProvideCityPerMonthReport(), None, msg="Return value should be None!")

        with patch("modules.load_balancer.LoadBalancer.GetAvailableWorker", return_value=Worker(id="1")):
            with patch("modules.worker.Worker.SelectCity", return_value=None):
                self.assertEqual(DatabaseAnalytics.ProvideCityPerMonthReport(), None,
                                 msg="Return value should be None!")

        with patch("modules.load_balancer.LoadBalancer.GetAvailableWorker", return_value=Worker(id="1")):
            with patch("modules.worker.Worker.SelectCity", return_value="Novi Sad"):
                self.assertEqual(DatabaseAnalytics.ProvideCityPerMonthReport(), None,
                                 msg="Return value should be None!")

    @patch("modules.database.Database.GetMeterConsumptionByMeter")
    @patch("modules.database_analitics.DatabaseAnalytics.GenerateEntityPerMonthReport")
    def test_ProvideMeterPerMonthReport(self, arg, arg1):
        with patch("modules.load_balancer.LoadBalancer.GetAvailableWorker", return_value=None):
            self.assertEqual(DatabaseAnalytics.ProvideMeterPerMonthReport(), None, msg="Return value should be None!")

        with patch("modules.load_balancer.LoadBalancer.GetAvailableWorker", return_value=Worker(id="1")):
            with patch("modules.worker.Worker.SelectMeter", return_value=None):
                self.assertEqual(DatabaseAnalytics.ProvideMeterPerMonthReport(), None,
                                 msg="Return value should be None!")

        with patch("modules.load_balancer.LoadBalancer.GetAvailableWorker", return_value=Worker(id="1")):
            with patch("modules.worker.Worker.SelectMeter", return_value=self.meter):
                self.assertEqual(DatabaseAnalytics.ProvideMeterPerMonthReport(), None,
                                 msg="Return value should be None!")

    @patch("os.system", return_value=None)
    @patch("builtins.print", return_value=None)
    @patch("builtins.input", return_value=None)
    @patch("modules.database_analitics.cursor", return_value=None)
    def test_GenerateEntityPerMonthReport(self, arg, arg1, arg2, arg3):
        self.assertEqual(DatabaseAnalytics.GenerateEntityPerMonthReport(self.meter, self.meter_consumptions), None,
                         msg="Return value should be None!")

        self.assertEqual(DatabaseAnalytics.GenerateEntityPerMonthReport(None, self.meter_consumptions), None,
                         msg="Return value should be None!")

        self.assertEqual(DatabaseAnalytics.GenerateEntityPerMonthReport(self.meter, []), None,
                         msg="Return value should be None!")


if __name__ == '__main__':
    unittest.main()
