import os

import splitting_problem as sp

PATH_TO_TASKS_DIR = os.path.join('tasks')
CSV_HEADER = ["N" , "n", "greedy_base", "dev", "greedy_custom", "dev", "iter_base", "dev", "iter_custom", "dev", "lower bound"]
FLOAT_LENGTH = 5

if __name__ == '__main__':
    task_files = os.listdir(PATH_TO_TASKS_DIR)

    greedy_base_dev = 0
    greedy_custom_dev = 0
    iter_base_dev = 0
    iter_custom_dev = 0

    with open('result.csv', 'w') as _file:
        _file.write('sep=,\n')
        _file.write(','.join(CSV_HEADER) + '\n')
        task_idx = 1
        for task_file in task_files:
            print(f'Working with {task_file}...')
            path_to_task = os.path.join(PATH_TO_TASKS_DIR, task_file)
            max_rod_length, workpiece_lengths = sp.read_task(path_to_task)

            lower_bound = sp.utils.get_lower_bound(workpiece_lengths, max_rod_length)
            base_permutation = [item for item in range(len(workpiece_lengths))]

            greedy_solver_base = sp.GreedySolver(workpiece_lengths,
                                        max_rod_length, sp.strategies.BaseOneStepStrat(workpiece_lengths))
            greedy_solver_custom = sp.GreedySolver(workpiece_lengths,
                                        max_rod_length, sp.strategies.CustomOneStepStrat(workpiece_lengths))
            iter_solver_base = sp.IterSolver(workpiece_lengths,
                                                max_rod_length, len(workpiece_lengths), sp.strategies.BaseMultiStepStrat())
            iter_solver_custom = sp.IterSolver(workpiece_lengths,
                                                max_rod_length, len(workpiece_lengths), sp.strategies.CustomMultiStepStrat(workpiece_lengths))

            greedy_solution_base, greedy_crit_base = greedy_solver_base.solve(base_permutation)
            greedy_solution_custom, greedy_crit_custom = greedy_solver_custom.solve(base_permutation)
            iter_solution_base, iter_crit_base = iter_solver_base.solve(base_permutation)
            iter_solution_custom, iter_crit_custom = iter_solver_custom.solve(base_permutation)

            cur_greedy_base_dev = sp.utils.get_deviation(greedy_crit_base, lower_bound)
            cur_greedy_custom_dev = sp.utils.get_deviation(greedy_crit_custom, lower_bound)
            cur_iter_base_dev = sp.utils.get_deviation(iter_crit_base, lower_bound)
            cur_iter_custom_dev = sp.utils.get_deviation(iter_crit_custom, lower_bound)

            _file.write(','.join([str(task_idx), str(len(workpiece_lengths)), str(greedy_crit_base), str(cur_greedy_base_dev)[:FLOAT_LENGTH],
                        str(greedy_crit_custom), str(cur_greedy_custom_dev)[:FLOAT_LENGTH], str(iter_crit_base), str(cur_iter_base_dev)[:FLOAT_LENGTH],
                        str(iter_crit_custom), str(cur_iter_custom_dev)[:FLOAT_LENGTH], str(lower_bound)]) + '\n')
            task_idx += 1

            greedy_base_dev += cur_greedy_base_dev
            greedy_custom_dev += cur_greedy_custom_dev
            iter_base_dev += cur_iter_base_dev
            iter_custom_dev += cur_iter_custom_dev

        _file.write(','.join(['', '', '', str(greedy_base_dev / (task_idx - 1))[:FLOAT_LENGTH],
                    '', str(greedy_custom_dev / (task_idx - 1))[:FLOAT_LENGTH], '',
                    str(iter_base_dev / (task_idx - 1))[:FLOAT_LENGTH], '', str(iter_custom_dev / (task_idx - 1))[:FLOAT_LENGTH]]))
