import os

import splitting_problem as sp

PATH_TO_TASKS_DIR = os.path.join('tasks')
CSV_HEADER = ["N" , "n", "one-step_base", "one-step_custom", "multi-step_base", "multi-step_custom", "lower bound"]

if __name__ == '__main__':
    task_files = os.listdir(PATH_TO_TASKS_DIR)
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
            multi_step_solver_base = sp.MultiStepSolver(workpiece_lengths,
                                                max_rod_length, len(workpiece_lengths), sp.strategies.BaseMultiStepStrat())

            one_step_solution_base, one_step_crit_base = one_step_solver_base.solve(base_permutation)
            multi_step_solution_base, multi_step_crit_base = multi_step_solver_base.solve(base_permutation)

            _file.write(','.join([str(task_idx), str(len(workpiece_lengths)), str(one_step_crit_base),
                        'NaN', str(multi_step_crit_base), 'NaN', str(lower_bound)]) + '\n')
            task_idx += 1
