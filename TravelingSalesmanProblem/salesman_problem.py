from argparse import ArgumentParser

from utils import get_crit
from salesman_task import SalesmanTask
from clustering import base_get_clusters
from solver import Solver

import numpy as np

import utils

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', required=True, type=str, help='Path to test task')
    return parser.parse_args()

def main():
    args = parse_arguments()
    task = SalesmanTask(args.input)
    solver = Solver(task, 8, 3)
    result = solver.solve()
    assert(len(set(result)) == len(result))

    print(f'crit: {get_crit(task.distances, result)}')

if __name__ == '__main__':
    main()
