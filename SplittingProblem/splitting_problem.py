import utils
import strategies

from argparse import ArgumentParser
from solvers import MultiStepSolver, OneStepSolver

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', required=True, type=str, help='Path to test task')
    return parser.parse_args()

def read_task(filename):
    with open(filename, 'r') as _file:
        lines = _file.readlines()
    assert(len(lines) == 1)
    task_data = lines[0].split()

    max_rod_length = int(task_data[0])
    workpiece_lengths_str = task_data[1:]
    return max_rod_length, list(map(int, workpiece_lengths_str))

def main():
    args = parse_arguments()

    max_rod_length, workpiece_lengths = read_task(args.input)
    base_permutation = [item for item in range(len(workpiece_lengths))]

    one_step_solver = OneStepSolver(workpiece_lengths,
                                    max_rod_length, strategies.BaseOneStepStrat(workpiece_lengths))

    one_step_solver_custom = OneStepSolver(workpiece_lengths,
                                    max_rod_length, strategies.CustomOneStepStrat(workpiece_lengths))
    multi_step_solver = MultiStepSolver(workpiece_lengths,
                                        max_rod_length, len(workpiece_lengths), strategies.BaseMultiStepStrat())
    multi_step_solver_custom = MultiStepSolver(workpiece_lengths,
                                        max_rod_length, len(workpiece_lengths), strategies.CustomMultiStepStrat(workpiece_lengths))

    one_step_solution, one_step_crit = one_step_solver.solve(base_permutation)
    one_step_solution_custom, one_step_crit_custom = one_step_solver_custom.solve(base_permutation)
    multi_step_solution, multi_step_crit = multi_step_solver.solve(base_permutation)
    multi_step_solution_custom, multi_step_crit_custom = multi_step_solver_custom.solve(base_permutation)

    print(f'One-step crit: {one_step_crit}')
    print(f'One-step custom crit: {one_step_crit_custom}')
    print(f'Multi-step crit: {multi_step_crit}')
    print(f'Multi-step crit custom: {multi_step_crit_custom}')

if __name__ == '__main__':
    main()
