import sys

sys.path.append("C:/Users/Milos/Documents/FAKULTET/3 godina/6_semestar/RES/Python/"
                "python-project-main-final/python-project-main")

from modules.worker import Worker
import unittest
from unittest.mock import patch
from models.meter import Meter


class TestWorker(unittest.TestCase):

    def setUp(self):
        self.worker = Worker('1')
        self.meter = Meter("1", "Nikola", "Tesla", "Cara Lazara", "13", "10100", "Beograd")

    @patch("time.sleep", return_value=None)
    @patch("modules.worker.Worker.ProcessMeterConsumption", return_value=None)
    def test_AddMeterConsumptions(self, arg, arg1):
        self.assertEqual(self.worker.AddMeterConsumptions([]), None, msg="Return value should be 'None'!")
        self.assertEqual(self.worker.AddMeterConsumptions(['1']), None, msg="Return value should be 'None'!")

    @patch("time.sleep", return_value=None)
    @patch("modules.database.Database.AddMeterConsumption", return_value=None)
    def test_ProcessMeterConsumption(self, arg, arg1):
        self.assertEqual(self.worker.ProcessMeterConsumption(self.meter), None, msg="Return value should be 'None'!")

    @patch("time.sleep", return_value=None)
    @patch("modules.database.Database.AddMeter", return_value=None)
    def test_ProcessMeterAdd(self, arg, arg1):
        self.assertEqual(self.worker.ProcessMeterAdd(self.meter), None, msg="Return value should be None!")

    @patch("time.sleep", return_value=None)
    @patch("modules.database.Database.UpdateMeter", return_value=None)
    def test_ProcessMeterUpdate(self, arg, arg1):
        self.assertEqual(self.worker.ProcessMeterUpdate(self.meter), None, msg="Return value should be None!")

    @patch("time.sleep", return_value=None)
    @patch("modules.database.Database.DeleteMeter", return_value=None)
    def test_ProcessMeterDelete(self, arg, arg1):
        self.assertEqual(self.worker.ProcessMeterDelete(self.meter), None, msg="Return value should be None!")

    @patch("modules.database.Database.GetAllMeters",
           return_value=[("1", "Nikola", "Tesla", "Cara Lazara", "13", "10100", "Beograd")])
    def test_GetAllMeters(self, arg):
        self.assertIsInstance(self.worker.GetAllMeters(), list, msg="Return value should be 'Meter' type!")
        self.assertEqual(type(self.worker.GetAllMeters()[0]), Meter, msg="Return value should be 'Meter' type!")
        self.assertEqual(self.worker.GetAllMeters()[0].id, self.meter.id, msg="Return value should be 'Meter' type!")

    def test_eq(self):
        self.assertEqual(self.worker.__eq__(None), False, msg="Return value should be False!")
        self.assertEqual(self.worker.__eq__(self.worker), True, msg="Return value should be True!")
        worker = Worker(id="2")
        self.assertEqual(self.worker.__eq__(worker), False, msg="Return value should be False!")

    def test_IsActive(self):
        self.assertEqual(self.worker.IsActive(), False, msg="Return value should be False!")
        self.worker.SwitchState()
        self.assertEqual(self.worker.IsActive(), True, msg="Return value should be False!")

    def test_SwitchState(self):
        self.assertEqual(self.worker.SwitchState(), None, msg="Return value should be None!")

    def test_StateChange(self):
        self.assertEqual(self.worker.StateChange(False), None, msg="Return value should be None!")
        self.assertEqual(self.worker.StateChange(False, True), None, msg="Return value should be None!")

    def test_TurnOn(self):
        self.assertEqual(self.worker.TurnOn(), None, msg="Return value should be None!")

    def test_TurnOff(self):
        self.assertEqual(self.worker.TurnOff(), None, msg="Return value should be None!")


if __name__ == '__main__':
    unittest.main()
