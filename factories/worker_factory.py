from modules.load_balancer import LoadBalancer
from modules.worker import Worker


class WorkerFactory:
    @staticmethod
    def MakeWorker(count: int):
        new_worker_id = 1
        for i in range(count):
            while new_worker_id in LoadBalancer.workers.keys():
                new_worker_id += 1
            new_worker = Worker(new_worker_id)
            LoadBalancer.workers[new_worker_id] = new_worker
