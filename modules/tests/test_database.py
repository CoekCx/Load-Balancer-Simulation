import sys

sys.path.append("C:/Users/Milos/Documents/FAKULTET/3 godina/6_semestar/RES/Python/"
                "python-project-main-final/python-project-main")

import unittest
from unittest.mock import patch
from modules.database import Database
from models.meter import Meter
from models.meter_consumption import DataPoint


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.meter = Meter("1", "Nikola", "Tesla", "Cara Lazara", "13", "10100", "Beograd")

    @patch("modules.database.Database.ProcessQuery", return_value=None)
    def test_AddMeter(self, arg):
        self.assertEqual(Database.AddMeter(self.meter), None, msg="Return value should be None!")

    @patch("modules.database.Database.ProcessQuery", return_value=None)
    def test_UpdateMeter(self, arg):
        self.assertEqual(Database.UpdateMeter(self.meter), None, msg="Return value should be None!")

    @patch("modules.database.Database.ProcessQuery", return_value=None)
    def test_DeleteMeter(self, arg):
        self.assertEqual(Database.DeleteMeter(self.meter), None, msg="Return value should be None!")

    def test_GetMeterKeys(self):
        with patch("modules.database.Database.ProcessQuery", return_value=[]):
            self.assertEqual(Database.GetMeterKeys(), [], msg="Return value should be empty list!")

        with patch("modules.database.Database.ProcessQuery", return_value=[['1', '2'], ['1', '2']]):
            self.assertEqual(Database.GetMeterKeys(), ['1', '1'], msg="Return value should be ['1', '1']!")

    @patch("modules.database.Database.ProcessQuery", return_value=None)
    def test_GetAllMeters(self, arg):
        self.assertEqual(Database.GetAllMeters(), None, msg="Return value should be None!")

    @patch("modules.database.Database.ProcessQuery", return_value=None)
    def test_AddMeterConsumption(self, arg):
        self.assertEqual(Database.AddMeterConsumption(DataPoint('1', 20, 'January')), None,
                         msg="Return value should be None!")

    def test_GetMeterConsumptionByMeter(self):
        with patch("modules.database.Database.ProcessQuery", return_value=[]):
            self.assertEqual(Database.GetMeterConsumptionByMeter('1'), [], msg="Return value should be empty list!")

        with patch("modules.database.Database.ProcessQuery",
                   return_value=[['1', 20, 'January'], ['1', 28, 'February']]):
            self.assertIsInstance(Database.GetMeterConsumptionByMeter('1'), list,
                                  msg="Return value should be None!")

    def test_GetMeterConsumptionByCity(self):
        with patch("modules.database.Database.ProcessQuery", return_value=[]):
            self.assertEqual(Database.GetMeterConsumptionByCity("Novi Sad"), [],
                             msg="Return value should be empty list!")

        with patch("modules.database.Database.ProcessQuery",
                   return_value=[['1', 20, 'January'], ['1', 28, 'February']]):
            self.assertIsInstance(Database.GetMeterConsumptionByCity("Novi Sad"), list,
                                  msg="Return value should be None!")

    @patch("modules.database.Database.ProcessQuery", return_value=None)
    def test_GetAllCities(self, arg):
        self.assertEqual(Database.GetAllCities(), None, msg="Return value should be None!")

    @patch("mysql.connector.cursor_cext.CMySQLCursor.execute", return_value=None)
    @patch("mysql.connector.cursor", return_value=None)
    @patch("mysql.connector.cursor_cext.CMySQLCursor.fetchall", return_value=None)
    @patch("mysql.connector.cursor_cext.CMySQLCursor.fetchone", return_value=None)
    @patch("mysql.connector.cursor.MySQLCursor.close", return_value=None)
    def test_ProcessQuery(self, arg, arg1, arg2, arg3, arg4):
        self.assertEqual(Database.ProcessQuery(""), None, msg="Return value should be None!")
        self.assertEqual(Database.ProcessQuery("", commit=True), None, msg="Return value should be None!")
        self.assertEqual(Database.ProcessQuery("", fetchall=True), None, msg="Return value should be None!")
        self.assertEqual(Database.ProcessQuery("", fetchone=True), None, msg="Return value should be None!")

    @patch("mysql.connector.cursor_cext.CMySQLCursor.execute", return_value=None)
    @patch("modules.database.print_message", return_value=None)
    def test_CreateTable(self, arg, arg1):
        with patch("mysql.connector.cursor", return_value=None):
            self.assertEqual(Database.CreateTable(), None, msg="Return value should be None!")
        with patch("mysql.connector.cursor", return_value=None):
            with patch('mysql.connector.cursor_cext.CMySQLCursor', **{'return_value.execute.side_effect': Exception()}):
                # with self.assertRaises(Exception):
                self.assertEqual(Database.CreateTable(), None, msg="Return value should be None!")


if __name__ == '__main__':
    unittest.main()
