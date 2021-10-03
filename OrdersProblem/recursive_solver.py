from orders_task import OrdersTask

class RecursiveSolver():
    def __init__(self, task: OrdersTask):
        self._my_permutation = None
        self._my_task = task
        self._backup_size = None
        self._my_cache = {}

    def _try_get_cached(self, current_order, current_performance):
        cached_profit, cached_solution = self._my_cache.get((current_order, current_performance), (None, None))
        if cached_profit is None:
            cached_profit, cached_solution = self._recursive_search(current_order, current_performance)
            self._my_cache[(current_order, current_performance)] = (cached_profit, cached_solution)

        return (cached_profit, cached_solution.copy()) \
            if self._my_task.orders_number < 100 else (cached_profit, cached_solution)

    def _recursive_search(self, current_order, current_performance):
        real_order = self._my_permutation[current_order]
        intensity = self._my_task.labour_intensity[real_order]
        est_profit = self._my_task.est_profit[real_order]

        if current_order == 0:
            solution = [False] * self._my_task.orders_number
            if intensity <= current_performance:
                solution[real_order] = True
                return (est_profit, solution)
            else:
                solution[real_order] = False
                return (0, solution)

        if intensity > current_performance:
            res_est_profit, res_solution = self._try_get_cached(current_order - 1, current_performance)
            res_solution[real_order] = False
            return res_est_profit, res_solution

        left_est_profit, left_solution = self._try_get_cached(current_order - 1, current_performance - intensity)
        left_est_profit += est_profit
        left_solution[real_order] = True

        right_est_profit, right_solution = self._try_get_cached(current_order - 1, current_performance)
        right_solution[real_order] = False

        return (left_est_profit, left_solution) if left_est_profit > right_est_profit \
            else (right_est_profit, right_solution)

    def solve(self, permutation, max_size=None):
        self._my_permutation = permutation
        if max_size:
            self._backup_size = self._my_task.orders_number
            self._my_task.orders_number = max_size

        crit, solution = self._recursive_search(self._my_task.orders_number - 1, self._my_task.max_performance)
        if max_size: self._my_task.orders_number = self._backup_size

        return crit, solution
