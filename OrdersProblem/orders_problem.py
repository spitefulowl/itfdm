import sys

from argparse import ArgumentParser
from recursive_solver import RecursiveSolver
from table_solver import TableSolver
from orders_task import OrdersTask
from strategies import BaseStrat
from strategies import CustomStrat

from math import ceil as math_ceil

sys.setrecursionlimit(3000)

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
    permutation = [item for item in range(task.orders_number)]
    base_permutation = BaseStrat.get_permutation(task)
    custom_permutation = CustomStrat.get_permutation(task)
    if task.orders_number < 20: print(f"Custom base permutation: {base_permutation}")
    recursive_solver = RecursiveSolver(task)
    table_solver = TableSolver(task)
    recursive_crit, recursive_solution = recursive_solver.solve(permutation)
    approx_recursive_crit, approx_recursive_solution = recursive_solver.solve(permutation, math_ceil(task.orders_number / 3))
    b_approx_recursive_crit, b_approx_recursive_solution = recursive_solver.solve(base_permutation, math_ceil(task.orders_number / 3))
    c_approx_recursive_crit, c_approx_recursive_solution = recursive_solver.solve(custom_permutation, math_ceil(task.orders_number / 3))
    table_crit, table_solution = table_solver.solve(permutation)
    print(f'Recursive crit: {recursive_crit}')
    print(f'Approx crit: {approx_recursive_crit}')
    print(f'Base approx crit: {b_approx_recursive_crit}')
    print(f'Custom approx crit: {c_approx_recursive_crit}')
    if task.orders_number < 20: print(f'Recursive solution: {recursive_solution}')
    print(f'Table crit: {table_crit}')
    if task.orders_number < 20: print(f'Table solution: {table_solution}')

if __name__ == "__main__":
    main()
