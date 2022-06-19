import sys
import threading
import time
from _thread import start_new_thread

sys.path.append("C:/Users/Milos/Documents/FAKULTET/3 godina/6_semestar/RES/Python/"
                "python-project-main-final/python-project-main")

import unittest
from modules.writer import Writer
from unittest.mock import patch
from modules.load_balancer import LoadBalancer
from modules.worker import Worker
from models.meter_consumption import DataPoint


class TestWriter(unittest.TestCase):
    def setUp(self):
        self.writer = Writer(id="1")

    @patch("modules.writer.Writer.ExecuteCleanMethod", return_value=None)
    def test_Execute(self, arg):
        self.assertEqual(self.writer.Execute(), None, msg="Return value should be None!")

    @patch("modules.writer.Writer.ViewWorkers", return_value=None)
    @patch('builtins.input', return_value=None)
    def test_ShowWorkerStatuses(self, arg, arg1):
        self.assertEqual(self.writer.ShowWorkerStatuses(), None, msg="Return value should be None!")

    @patch("os.system", return_value=None)
    @patch("modules.writer.print_in_color")
    @patch("builtins.print", return_value=None)
    def test_ViewWorkers(self, arg, arg1, arg2):
        with patch.object(LoadBalancer, "workers", {'worker 1': Worker(id="1")}):
            start_new_thread(TestWriter.ViewWorkersHelper, ())
            self.assertEqual(self.writer.ViewWorkers(), None, msg="Return value should be None!")
        with patch.object(LoadBalancer, "workers", {}):
            start_new_thread(TestWriter.ViewWorkersHelper, ())
            self.assertEqual(self.writer.ViewWorkers(), None, msg="Return value should be None!")

    @staticmethod
    def ViewWorkersHelper():
        Worker.update_view = True
        time.sleep(0.6)
        Writer.stop_showing_workers = True

    @patch("modules.writer.Writer.ShowWorkerStatuses", return_value=None)
    @patch("modules.writer.print_message", return_value=None)
    def test_SendData(self, arg, arg1):
        with patch("modules.load_balancer.LoadBalancer.GetAvailableWorker", return_value=Worker(id="1")):
            with patch("modules.writer.Writer.InputDataEntry", return_value=DataPoint("1", 2, "3")):
                with patch("modules.load_balancer.LoadBalancer.ReceiveData", return_value=True):
                    self.assertEqual(self.writer.SendData(), None, msg="Return value should be None!")

        with patch("modules.load_balancer.LoadBalancer.GetAvailableWorker", return_value=None):
            self.assertEqual(self.writer.SendData(), None, msg="Return value should be None!")

        with patch("modules.load_balancer.LoadBalancer.GetAvailableWorker", return_value=Worker(id="1")):
            with patch("modules.writer.Writer.InputDataEntry", return_value=None):
                self.assertEqual(self.writer.SendData(), None, msg="Return value should be None!")

        with patch("modules.load_balancer.LoadBalancer.GetAvailableWorker", return_value=Worker(id="1")):
            with patch("modules.writer.Writer.InputDataEntry", return_value=DataPoint("1", 2, "3")):
                with patch("modules.load_balancer.LoadBalancer.ReceiveData", return_value=False):
                    self.assertEqual(self.writer.SendData(), None, msg="Return value should be None!")

    def test_UpdateWorkerStates(self):
        statuses = [Worker(id="1")]
        with patch.object(LoadBalancer, "workers", {'worker 1': Worker(id="1")}):
            self.assertEqual(self.writer.UpdateWorkerStates(statuses), None, msg="Return value should be None!")

        with patch.object(LoadBalancer, "workers", {}):
            self.assertEqual(self.writer.UpdateWorkerStates(statuses), None, msg="Return value should be None!")

    @patch("modules.writer.Writer.ShowWorkerStatuses", return_value=None)
    @patch("os.system", return_value=None)
    def test_ExecuteCleanMethod(self, arg, arg1):
        self.assertEqual(self.writer.ExecuteCleanMethod(self.writer.ShowWorkerStatuses), None,
                         msg="Return value should be None!")

        with patch("modules.writer.Writer.Execute", return_value=None):
            self.assertEqual(self.writer.ExecuteCleanMethod(TestWriter.ThrowException), None,
                             msg="Return value should be None!")

    @staticmethod
    def ThrowException():
        raise KeyboardInterrupt

    def test_Close(self):
        self.assertEqual(self.writer.Close(), None, msg="Return value should be None!")


if __name__ == '__main__':
    unittest.main()
