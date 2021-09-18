import utils
import strategies

from argparse import ArgumentParser
from solvers import OneStepSolver

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
    one_step_solver = OneStepSolver(workpiece_lengths, max_rod_length, strategies.base_onestep_strat)
    solution, crit = one_step_solver.solve(base_permutation)
    print(solution)
    print(crit)

if __name__ == '__main__':
    main()
