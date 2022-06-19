import sys

sys.path.append("C:/Users/Milos/Documents/FAKULTET/3 godina/6_semestar/RES/Python/"
                "python-project-main-final/python-project-main")
import unittest
from unittest.mock import patch
from modules.load_balancer import LoadBalancer
from modules.worker import Worker


class TestLoadBalancer(unittest.TestCase):

    @patch("modules.load_balancer.print_error", return_value=None)
    @patch("modules.load_balancer.print_message", return_value=None)
    def test_ReceiveData(self, mocked, mocked1):
        with patch.object(LoadBalancer, "buffer", [0, 1]):
            self.assertEqual(LoadBalancer.ReceiveData(1), None, msg="Return value should be 'None'!")
        with patch.object(LoadBalancer, "buffer", [0, 1, 2, 3]):
            self.assertEqual(LoadBalancer.ReceiveData(4), True, msg="Return value should be 'True'!")

    @patch("modules.load_balancer.LoadBalancer.CheckForInactivateWorker", return_value=None)
    @patch("modules.load_balancer.LoadBalancer.CheckForAvailableWorker", return_value=None)
    def test_GetWorker(self, mocked, mocked1):
        self.assertEqual(LoadBalancer.GetWorker(), None, msg="Return value should be 'None'!")
        mocked.return_value = Worker('1', active=False)
        self.assertIsInstance(LoadBalancer.GetWorker(), Worker, msg="Return value should be 'Worker' class type!")

    def test_CheckForAvailableWorker(self):
        with patch.object(LoadBalancer, "workers", {}):
            self.assertEqual(LoadBalancer.CheckForAvailableWorker(), None, msg="Return value should be 'None'!")
        worker = Worker(id="1")
        worker.TurnOn()
        worker.busy = False
        with patch.object(LoadBalancer, "workers", {"Worker 1": worker}):
            self.assertEqual(LoadBalancer.CheckForAvailableWorker(), worker, msg="Return value should be 'None'!")
        worker.busy = True
        with patch.object(LoadBalancer, "workers", {"Worker 1": worker}):
            self.assertEqual(LoadBalancer.CheckForAvailableWorker(), None, msg="Return value should be 'None'!")

    def test_CheckForInactivateWorker(self):
        with patch.object(LoadBalancer, "workers", {}):
            self.assertEqual(LoadBalancer.CheckForInactivateWorker(), None, msg="Return value should be 'None'!")
        worker = Worker(id="1")
        with patch.object(LoadBalancer, "workers", {"Worker 1": worker}):
            self.assertEqual(LoadBalancer.CheckForInactivateWorker(), worker, msg="Return value should be 'None'!")
        worker.TurnOn()
        with patch.object(LoadBalancer, "workers", {"Worker 1": worker}):
            self.assertEqual(LoadBalancer.CheckForInactivateWorker(), None, msg="Return value should be 'None'!")

    @patch("modules.load_balancer.LoadBalancer.CheckForAvailableWorker", return_value=None)
    @patch("modules.load_balancer.print_error", return_value=None)
    @patch("modules.load_balancer.print_message", return_value=None)
    @patch("modules.worker.Worker.ProcessWorkerAction", return_value=None)
    def test_ProcessData(self, worker, print_message, print_error, mocked):
        with patch.object(LoadBalancer, "buffer", ['0']):
            with patch("modules.load_balancer.LoadBalancer.CheckForAvailableWorker", return_value=None):
                self.assertEqual(LoadBalancer.ProcessData(), None, msg="Return value should be 'None'!")

        with patch.object(LoadBalancer, "buffer", ['0']):
            with patch("modules.load_balancer.LoadBalancer.CheckForAvailableWorker", return_value=Worker(id='1')):
                with patch("modules.load_balancer.LoadBalancer.GetWorker", return_value=Worker(id='1')):
                    self.assertEqual(LoadBalancer.ProcessData(), None, msg="Return value should be 'None'!")


if __name__ == '__main__':
    unittest.main(verbosity=2)
