from os import read
import numpy as np
from argparse import ArgumentParser

from delivery_task import DeliveryTask

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

if __name__ == "__main__":
    main()
