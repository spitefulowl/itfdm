from orders_task import OrdersTask

class BaseStrat():
    @staticmethod
    def get_permutation(task: OrdersTask):
        permutation = [idx for idx in range(task.orders_number)]
        return sorted(permutation, key=lambda x: task.labour_intensity[x] / task.est_profit[x], reverse=True)
