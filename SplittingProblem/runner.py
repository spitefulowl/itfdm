import os

import splitting_problem as sp

PATH_TO_TASKS_DIR = os.path.join('tasks')
CSV_HEADER = ["N" , "n", "one-step_base", "dev", "one-step_custom", "dev", "multi-step_base", "dev", "multi-step_custom", "dev", "lower bound"]
FLOAT_LENGTH = 5

if __name__ == '__main__':
    task_files = os.listdir(PATH_TO_TASKS_DIR)

    one_step_base_dev = 0
    one_step_custom_dev = 0
    multi_step_base_dev = 0
    multi_step_custom_dev = None

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

            one_step_solver_base = sp.OneStepSolver(workpiece_lengths,
                                        max_rod_length, sp.strategies.BaseOneStepStrat(workpiece_lengths))
            one_step_solver_custom = sp.OneStepSolver(workpiece_lengths,
                                        max_rod_length, sp.strategies.CustomOneStepStrat(workpiece_lengths))
            multi_step_solver_base = sp.MultiStepSolver(workpiece_lengths,
                                                max_rod_length, len(workpiece_lengths), sp.strategies.BaseMultiStepStrat())

            one_step_solution_base, one_step_crit_base = one_step_solver_base.solve(base_permutation)
            one_step_solution_custom, one_step_crit_custom = one_step_solver_custom.solve(base_permutation)
            multi_step_solution_base, multi_step_crit_base = multi_step_solver_base.solve(base_permutation)

            cur_one_step_base_dev = sp.utils.get_deviation(one_step_crit_base, lower_bound)
            cur_one_step_custom_dev = sp.utils.get_deviation(one_step_crit_custom, lower_bound)
            cur_multi_step_base_dev = sp.utils.get_deviation(multi_step_crit_base, lower_bound)
            multi_step_custom_dev = "NaN"

            _file.write(','.join([str(task_idx), str(len(workpiece_lengths)), str(one_step_crit_base), str(cur_one_step_base_dev)[:FLOAT_LENGTH],
                        str(one_step_crit_custom), str(cur_one_step_custom_dev)[:FLOAT_LENGTH], str(multi_step_crit_base), str(cur_multi_step_base_dev)[:FLOAT_LENGTH],
                        'NaN', str(multi_step_custom_dev)[:FLOAT_LENGTH], str(lower_bound)]) + '\n')
            task_idx += 1

            one_step_base_dev += cur_one_step_base_dev
            one_step_custom_dev += cur_one_step_custom_dev
            multi_step_base_dev += cur_multi_step_base_dev
            multi_step_custom_dev = None

        _file.write(','.join(['', '', '', str(one_step_base_dev / (task_idx - 1))[:FLOAT_LENGTH],
                    '', str(one_step_custom_dev / (task_idx - 1))[:FLOAT_LENGTH], '',
                    str(multi_step_base_dev / (task_idx - 1))[:FLOAT_LENGTH], '', 'Nan']))
