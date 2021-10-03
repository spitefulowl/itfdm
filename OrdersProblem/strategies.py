from orders_task import OrdersTask

class BaseStrat():
    @staticmethod
    def get_permutation(task: OrdersTask):
        permutation = [idx for idx in range(task.orders_number)]
        return sorted(permutation, key=lambda x: task.est_profit[x] / task.labour_intensity[x], reverse=True)

class CustomStrat():
    @staticmethod
    def get_permutation(task: OrdersTask):
        permutation = BaseStrat.get_permutation(task)
        est_profit = task.est_profit.copy()
        est_profit.sort()
        median_profit = est_profit[int(len(est_profit) / 2)]
        result_permutation = []
        for item in permutation[:int(len(permutation) / 2)]:
            if task.est_profit[item] > median_profit:
                result_permutation.insert(0, item)
            else:
                result_permutation.append(item)

        return result_permutation + permutation[int(len(permutation) / 2):]
