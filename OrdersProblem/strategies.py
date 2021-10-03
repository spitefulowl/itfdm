from orders_task import OrdersTask

class BaseStrat():
    @staticmethod
    def get_permutation(task: OrdersTask):
        permutation = [idx for idx in range(task.orders_number)]
        est_profit = []
        for profit in task.est_profit:
            if profit == 0: est_profit.append(0.000001)
            else: est_profit.append(profit)
        return sorted(permutation, key=lambda x: task.labour_intensity[x] / (est_profit[x]), reverse=False)

class CustomStrat():
    @staticmethod
    def get_permutation(task: OrdersTask):
        permutation = BaseStrat.get_permutation(task)
        avg_profit = sum(task.est_profit) / len(task.est_profit)
        result_permutation = []
        for item in permutation[:int(len(permutation) / 2)]:
            if task.est_profit[item] > avg_profit:
                result_permutation.insert(0, item)
            else:
                result_permutation.append(item)
        return result_permutation + permutation[int(len(permutation) / 2):]
