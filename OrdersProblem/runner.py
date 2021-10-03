import os

from timeit import default_timer as timer

import orders_problem as op

def get_ratio(opt_crit, approx_crit) -> float:
    return opt_crit / approx_crit

PATH_TO_TASKS_DIR = os.path.join('Task3')
CSV_HEADER = ["N" , "n", "recursive", "time", "table", "time", "approx_base", "time", "ratio", "approx_custom", "time", "ratio"]
FLOAT_LENGTH = 9
TIMER_RES = 1000

if __name__ == '__main__':
    task_files = os.listdir(PATH_TO_TASKS_DIR)

    with open('result.csv', 'w') as _file:
        _file.write('sep=,\n')
        _file.write(','.join(CSV_HEADER) + '\n')
        task_idx = 1
        for task_file in task_files:
            print(f'Working with {task_file}...')
            path_to_task = os.path.join(PATH_TO_TASKS_DIR, task_file)
            task = op.read_task(path_to_task)
            base_permutation = [item for item in range(task.orders_number)]

            rec_time_start = timer()
            recursive_crit, _ = op.RecursiveSolver(task).solve(base_permutation)
            rec_time_end = timer()

            tab_time_start = timer()
            table_crit, _ = op.TableSolver(task).solve(base_permutation)
            tab_time_end = timer()

            _file.write(','.join(map(str, [task_idx, task.orders_number, \
                    recursive_crit, str((rec_time_end - rec_time_start) * TIMER_RES)[:FLOAT_LENGTH], \
                    table_crit, str((tab_time_end - tab_time_start) * TIMER_RES)[:FLOAT_LENGTH], '\n'])))

            task_idx += 1
