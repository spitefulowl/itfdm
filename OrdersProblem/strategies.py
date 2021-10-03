from orders_task import OrdersTask

class BaseStrat():
    @staticmethod
    def get_permutation(task: OrdersTask):
        permutation = [idx for idx in range(task.orders_number)]
        return sorted(permutation, key=lambda x: task.labour_intensity[x] / (task.est_profit[x] + 1), reverse=False)

class CustomStrat():
    @staticmethod
    def get_permutation(task: OrdersTask):
        permutation = [idx for idx in range(task.orders_number)]
        return sorted(permutation, key=lambda x: task.est_profit[x] + 1, reverse=False)
