import sys

sys.path.append("C:/Users/Milos/Documents/FAKULTET/3 godina/6_semestar/RES/Python/"
                "python-project-main-final/python-project-main")

import unittest
from unittest.mock import patch
from factories.worker_factory import WorkerFactory
from modules.load_balancer import LoadBalancer
from modules.worker import Worker


class TestWorkerFactory(unittest.TestCase):
    def test_MakeWorker(self):
        self.assertEqual(WorkerFactory.MakeWorker(1), None, msg="Return value should be None!")
        self.assertEqual(WorkerFactory.MakeWorker(0), None, msg="Return value should be None!")
        with patch.object(LoadBalancer, "workers", {1: Worker(id="1")}):
            self.assertEqual(WorkerFactory.MakeWorker(1), None, msg="Return value should be None!")


if __name__ == '__main__':
    unittest.main()
