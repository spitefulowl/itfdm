from os import read
import numpy as np
from argparse import ArgumentParser

from delivery_task import DeliveryTask
from branch_and_bound import BranchAndBound
from utils import get_crit

import lower_bounds as lb
import upper_bounds as ub
import tree_traversals as tt

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', required=True, type=str, help='Path to test task')
    return parser.parse_args()

def read_task(filename):
    with open(filename, 'r') as _file:
        lines = _file.readlines()

    size = int(lines[0].strip())
    target_dates = list(map(int, lines[1].strip().split()))

    delivery_matrix = []
    for idx in range(size + 1):
        delivery_matrix.append(list(map(int, lines[2 + idx].strip().split('\t'))))
    delivery_matrix = np.mat(delivery_matrix)

    return DeliveryTask(size, target_dates, delivery_matrix)

def main():
    args = parse_arguments()
    task = read_task(args.input)
    if task.size < 10:
        print(task)

    lower_bound = lb.BaseLowerBound(task)
    upper_bound = ub.BaseUpperBound(task)
    strategy = tt.BreadthFirst()

    solution = BranchAndBound.solve(task.size, strategy, lower_bound, upper_bound)
    print(solution, get_crit(task, solution))

if __name__ == "__main__":
    main()
