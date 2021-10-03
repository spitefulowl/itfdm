import os

from timeit import default_timer as timer

from strategies import BaseStrat
from strategies import CustomStrat
import orders_problem as op

def get_ratio(opt_crit, approx_crit) -> float:
    return opt_crit / approx_crit

PATH_TO_TASKS_DIR = os.path.join('Task3')
CSV_HEADER = ["N" , "n", "recursive", "time", "table", "time", "approx_base", "time", "ratio", "approx_custom", "time", "ratio"]
FLOAT_LENGTH = 9
TIMER_RES = 1000

if __name__ == '__main__':
    task_files = os.listdir(PATH_TO_TASKS_DIR)

    ratio_base_avg = 0
    ratio_custom_avg = 0

    with open('result.csv', 'w') as _file:
        _file.write('sep=,\n')
        _file.write(','.join(CSV_HEADER) + '\n')
        task_idx = 1
        for task_file in task_files:
            print(f'Working with {task_file}...')
            path_to_task = os.path.join(PATH_TO_TASKS_DIR, task_file)
            task = op.read_task(path_to_task)
            permutation = [item for item in range(task.orders_number)]
            base_permutation = BaseStrat.get_permutation(task)
            custom_permutation = CustomStrat.get_permutation(task)

            rec_time_start = timer()
            recursive_crit, _ = op.RecursiveSolver(task).solve(permutation)
            rec_time_end = timer()

            tab_time_start = timer()
            table_crit, _ = op.TableSolver(task).solve(permutation)
            tab_time_end = timer()

            ba_time_start = timer()
            base_approx_crit, _ = op.RecursiveSolver(task).solve(base_permutation, op.math_ceil(task.orders_number / 3))
            ba_time_end = timer()

            bc_time_start = timer()
            custom_approx_crit, _ = op.RecursiveSolver(task).solve(custom_permutation, op.math_ceil(task.orders_number / 3))
            bc_time_end = timer()

            ratio_ba = base_approx_crit / recursive_crit
            ratio_bc = custom_approx_crit / recursive_crit

            ratio_base_avg += ratio_ba
            ratio_custom_avg += ratio_bc

            _file.write(','.join(map(str, [task_idx, task.orders_number, \
                    recursive_crit, str((rec_time_end - rec_time_start) * TIMER_RES)[:FLOAT_LENGTH], \
                    table_crit, str((tab_time_end - tab_time_start) * TIMER_RES)[:FLOAT_LENGTH], \
                    base_approx_crit, str((ba_time_end - ba_time_start) * TIMER_RES)[:FLOAT_LENGTH], str(ratio_ba)[:FLOAT_LENGTH],
                    custom_approx_crit, str((bc_time_end - bc_time_start) * TIMER_RES)[:FLOAT_LENGTH], str(ratio_bc)[:FLOAT_LENGTH],
                    '\n'])))

            task_idx += 1
        _file.write(','.join(map(str, [''] * 8 + [str(ratio_base_avg / (task_idx - 1))[:FLOAT_LENGTH], '', '', str(ratio_custom_avg / (task_idx - 1))[:FLOAT_LENGTH]])))
