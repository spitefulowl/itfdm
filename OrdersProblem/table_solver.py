from orders_task import OrdersTask

class TableSolver():
    def __init__(self, task: OrdersTask):
        self._my_permutation = None
        self._my_task = task
        self._backup_size = None

    def solve(self, permutation, max_size=None):
        self._my_permutation = permutation
        if max_size:
            self._backup_size = self._my_task.orders_number
            self._my_task.orders_number = max_size

        real_first_idx = permutation[0]
        real_first_est = self._my_task.est_profit[real_first_idx]
        real_first_intensity = self._my_task.labour_intensity[real_first_idx]

        second_column = []
        for current_performance in range(self._my_task.max_performance):
            append_profit = real_first_est if real_first_intensity <= current_performance + 1 else 0
            append_solution = { real_first_idx: True } if real_first_intensity <= current_performance + 1 else { real_first_idx: False }
            second_column.append([append_profit, append_solution])

        first_column = [None] * self._my_task.max_performance
        for idx in range(len(first_column)):
            first_column[idx] = [0, {}]

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
                    second_option = first_column[current_performance][0]
                    if first_option > second_option:
                        second_column[current_performance][0] = first_option
                        second_column[current_performance][1] = { real_order: True }
                    else:
                        second_column[current_performance][0] = second_option
                        second_column[current_performance][1].clear()
                        second_column[current_performance][1].update(first_column[current_performance][1])
                    continue

                second_option = first_column[current_performance][0]
                second_column[current_performance][1].clear()
                if intensity < current_performance + 1:
                    first_option = first_column[current_performance - intensity][0] + est_profit
                    if first_option > second_option:
                        second_column[current_performance][0] = first_option
                        second_column[current_performance][1].update(first_column[current_performance - intensity][1])
                        second_column[current_performance][1].update({ real_order: True })
                        continue
                second_column[current_performance][0] = second_option
                second_column[current_performance][1].update(first_column[current_performance][1])

        for idx in range(0, self._my_task.orders_number):
            if idx not in second_column[current_performance][1].keys():
                second_column[current_performance][1][idx] = False

        if max_size:
            self._my_task.orders_number = self._backup_size

        return second_column[-1]
