import os

import salesman_problem as sp

PATH_TO_TASKS_DIR = os.path.join('tasks')
CSV_HEADER = ["task" , "base", "base_dev", "custom", "custom_dev", "optimal"]
SOLUTIONS = {
    "dj38.tsp": 6656,
    "ei8246.tsp": 206171,
    "uy734.tsp": 79114,
    "xqf131.tsp": 564,
    "xqg237.tsp": 1019,
    "xql662.tsp": 2513
}

FLOAT_LENGTH = 5

if __name__ == '__main__':
    task_files = os.listdir(PATH_TO_TASKS_DIR)

    base_dev_sum = 0
    custom_dev_sum = 0

    with open('result.csv', 'w') as _file:
        _file.write('sep=,\n')
        _file.write(','.join(CSV_HEADER) + '\n')
        task_idx = 1
        for task_file in task_files:
            print(f'Working with {task_file}...')
            path_to_task = os.path.join(PATH_TO_TASKS_DIR, task_file)
            task = sp.SalesmanTask(path_to_task)
            base_solver = sp.Solver(task, 8, 3)
            base_crit = sp.utils.get_crit(task.distances, base_solver.solve())
            base_dev = 1 - SOLUTIONS[task_file] / base_crit
            base_dev_sum += base_dev

            custom_solver = sp.Solver(task, 8, 3, sp.custom_get_clusters, sp.utils.custom_selector)
            custom_crit = sp.utils.get_crit(task.distances, custom_solver.solve())
            custom_dev = 1 - SOLUTIONS[task_file] / custom_crit
            custom_dev_sum += custom_dev

            _file.write(','.join(map(str, [task_file, base_crit, base_dev, custom_crit, custom_dev, SOLUTIONS[task_file]])) + '\n')

        base_dev_avg = base_dev_sum / len(task_files)
        custom_dev_avg = custom_dev_sum / len(task_files)
        _file.write(','.join(map(str, ['', '', base_dev_avg, '', custom_dev_avg])) + '\n')
