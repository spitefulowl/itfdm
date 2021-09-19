import utils
import strategies

from argparse import ArgumentParser
from solvers import IterSolver, GreedySolver

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

    greedy_solver = GreedySolver(workpiece_lengths,
                                    max_rod_length, strategies.BaseOneStepStrat(workpiece_lengths))

    greedy_solver_custom = GreedySolver(workpiece_lengths,
                                    max_rod_length, strategies.CustomOneStepStrat(workpiece_lengths))
    iter_solver = IterSolver(workpiece_lengths,
                                        max_rod_length, len(workpiece_lengths), strategies.BaseMultiStepStrat())
    iter_solver_custom = IterSolver(workpiece_lengths,
                                        max_rod_length, len(workpiece_lengths), strategies.CustomMultiStepStrat(workpiece_lengths))

    greedy_solution, greedy_crit = greedy_solver.solve(base_permutation)
    greedy_solution_custom, greedy_crit_custom = greedy_solver_custom.solve(base_permutation)
    iter_solution, iter_crit = iter_solver.solve(base_permutation)
    iter_solution_custom, iter_crit_custom = iter_solver_custom.solve(base_permutation)

    print(f'Greedy crit: {greedy_crit}')
    print(f'Greedy custom crit: {greedy_crit_custom}')
    print(f'Iter crit: {iter_crit}')
    print(f'Iter crit custom: {iter_crit_custom}')

if __name__ == '__main__':
    main()
