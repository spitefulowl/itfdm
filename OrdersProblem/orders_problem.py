import sys

from argparse import ArgumentParser
from recursive_solver import RecursiveSolver
from orders_task import OrdersTask

sys.setrecursionlimit(1500)

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', required=True, type=str, help='Path to test task')
    return parser.parse_args()

def read_task(filename):
    with open(filename, 'r') as _file:
        lines = _file.readlines()
    assert(len(lines) == 4)
    max_performance = int(lines[0].strip())
    orders_number = int(lines[1].strip())
    labour_intensity = list(map(int, lines[2].strip().split()))
    est_profit = list(map(int, lines[3].strip().split()))
    assert(len(labour_intensity) == len(est_profit) == orders_number)
    return OrdersTask(max_performance, orders_number, labour_intensity, est_profit)

def main():
    args = parse_arguments()
    task = read_task(args.input)
    if task.orders_number < 20: print(task)
    base_permutation = [item for item in range(task.orders_number)]
    recursive_solver = RecursiveSolver(task)
    recursive_crit, recursive_solution = recursive_solver.solve(base_permutation)
    print(f'Crit: {recursive_crit}')
    if task.orders_number < 20: print(f'Solution: {recursive_solution}')

if __name__ == "__main__":
    main()
