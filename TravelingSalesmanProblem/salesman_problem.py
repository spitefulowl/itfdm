from argparse import ArgumentParser

from salesman_task import SalesmanTask
from clustering import base_get_clusters

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', required=True, type=str, help='Path to test task')
    return parser.parse_args()

def main():
    args = parse_arguments()
    task = SalesmanTask(args.input)
    points = [idx for idx in range(len(task.distances))]
    base_get_clusters(points, task.distances, 8)

if __name__ == '__main__':
    main()
