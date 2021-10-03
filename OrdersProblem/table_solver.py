from orders_task import OrdersTask

class TableSolver():
    def __init__(self, task: OrdersTask):
        self._my_permutation = None
        self._my_task = task
        self._my_cache = {}

    def solve(self, permutation):
        self._my_permutation = permutation

        real_first_idx = permutation[0]
        real_first_est = self._my_task.est_profit[real_first_idx]
        real_first_intensity = self._my_task.labour_intensity[real_first_idx]

        second_column = []
        for current_performance in range(self._my_task.max_performance):
            append_profit = real_first_est if real_first_intensity <= current_performance + 1 else 0
            # append_soluti

            second_column.append(append_profit)

        first_column = [0] * self._my_task.max_performance

        for column_idx in range(1, self._my_task.orders_number):
            tmp = second_column
            second_column = first_column
            first_column = tmp
            for current_performance in range(self._my_task.max_performance):
                real_order = permutation[column_idx]
                intensity = self._my_task.labour_intensity[real_order]
                est_profit = self._my_task.est_profit[real_order]

                if intensity == current_performance + 1:
                    first_option = est_profit
                    second_option = first_column[current_performance]
                    second_column[current_performance] = max(first_option, second_option)
                    continue

                if intensity < current_performance + 1:
                    first_option = first_column[current_performance - intensity] + est_profit
                    second_option = first_column[current_performance]
                    second_column[current_performance] = max(first_option, second_option)
                else:
                    second_column[current_performance] = first_column[current_performance]

        print(second_column)