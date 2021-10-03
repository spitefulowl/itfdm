from orders_task import OrdersTask

class BaseStrat():
    @staticmethod
    def get_permutation(task: OrdersTask):
        permutation = [idx for idx in range(task.orders_number)]
        return sorted(permutation, key=lambda x: task.labour_intensity[x] / (task.est_profit[x] + 1), reverse=False)

class CustomStrat():
    @staticmethod
    def get_permutation(task: OrdersTask):
        permutation = BaseStrat.get_permutation(task)
        permutation = sorted(permutation[:int(len(permutation) / 2)], key=lambda x: task.labour_intensity[x], reverse=False)
        avg_profit = sum(task.est_profit) / len(task.est_profit)
        result_permutation = []
        for item in permutation:
            if task.est_profit[item] > avg_profit:
                result_permutation.insert(0, item)
            else:
                result_permutation.append(item)
        return result_permutation + permutation[int(len(permutation) / 2):]
