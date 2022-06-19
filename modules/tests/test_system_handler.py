import sys

sys.path.append("C:/Users/Milos/Documents/FAKULTET/3 godina/6_semestar/RES/Python/"
                "python-project-main-final/python-project-main")

import unittest
from modules.system_handler import SystemHandler
from unittest.mock import patch
from modules.writer import Writer
from models.meter import Meter


class TestSystemHandler(unittest.TestCase):

    def setUp(self):
        self.system_handler = SystemHandler()
        self.writer = Writer("1")

    @patch("modules.system_handler.SystemHandler.ExecuteCleanMethod", return_value=None)
    def test_Execute(self, arg):
        self.assertEqual(self.system_handler.Execute(), None, msg="Return value should be None!")

    def test_RemoveWritersFromDictionary(self):
        with patch.object(self.system_handler, "writers", {"1": self.writer}):
            self.assertEqual(self.system_handler.RemoveWritersFromDictionary([self.writer]), None,
                             msg="Return value should be None!")

        with patch.object(self.system_handler, "writers", {}):
            self.assertEqual(self.system_handler.RemoveWritersFromDictionary([self.writer]), None,
                             msg="Return value should be None!")

        with patch.object(self.system_handler, "writers", {"2": self.writer}):
            with self.assertRaises(KeyError):
                self.system_handler.RemoveWritersFromDictionary([self.writer])

    def test_ParseUpdatedMeter(self):
        meter = Meter("1", "Nikola", "Tesla", "Cara Lazara", "13", "10100", "Beograd")
        data = {'city': "NoviSad", 'first_name': "Jovan", 'last_name': "Jovanovic",
                'street_name': "Bulevar Cara Lazara", 'street_number': "12", 'zip_code': "123"}
        data_bad = {'city': "NoviSad", 'first_name': "Jovan", 'last_name': "Jovanovic",
                    'street_name': "Bulevar Cara Lazara", 'str': "12", 'zip_code': "123"}
        self.assertEqual(self.system_handler.ParseUpdatedMeter(meter, data), None, msg="Return value should be None!")

        with self.assertRaises(KeyError):
            self.system_handler.ParseUpdatedMeter(meter, data_bad)

    @patch("modules.system_handler.DatabaseAnalytics.ProvideCityPerMonthReport", return_value=None)
    def test_GetCityReport(self, arg):
        self.assertEqual(self.system_handler.GetCityReport(), None, msg="Return value should be None!")

    @patch("modules.system_handler.DatabaseAnalytics.ProvideMeterPerMonthReport", return_value=None)
    def test_GetMeterReport(self, arg):
        self.assertEqual(self.system_handler.GetMeterReport(), None, msg="Return value should be None!")

    @patch("modules.system_handler.DatabaseAnalytics.ProvideCityPerMonthReport", return_value=None)
    @patch("os.system", return_value=None)
    def test_ExecuteCleanMethod(self, arg, arg1):
        self.assertEqual(self.system_handler.ExecuteCleanMethod(self.system_handler.GetCityReport), None,
                         msg="Return value should be None!")
        with patch("modules.system_handler.SystemHandler.Execute", return_value=None):
            with self.assertRaises(TypeError):
                self.system_handler.ExecuteCleanMethod(self.raise_exception)

    def raise_exception(self):
        raise TypeError


if __name__ == '__main__':
    unittest.main()
