from argparse import ArgumentParser
from os import listdir as os_listdir
from re import compile as re_compile
from math import factorial as math_factorial

import subprocess

ITERATIONS_PATTERN = re_compile("Iterations: (\\d+)")
CRIT_PATTERN = re_compile("Crit: (\\d+)")
TASK_SIZE_PATTERN = re_compile("task_2_\\d+_n(\\d+).txt")

ALGO_SET = ("base",)
CSV_HEADER = ["n", "base_iter", "ratio", "custom_iter", "ratio"]
FLOAT_LENGTH = 9

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('-b', '--binary', required=True, type=str, help='Path to binary')
    parser.add_argument('-t', '--tasks', required=True, type=str, help='Path to test task')
    return parser.parse_args()

def parse_output(stdout):
    output = str(stdout)
    iterations = ITERATIONS_PATTERN.search(output).group(1)
    crit = CRIT_PATTERN.search(output).group(1)
    return (iterations, crit)

def save_csv(results):
    with open("results.csv", "w") as _file:
        _file.write('sep=,\n')
        _file.write(','.join(CSV_HEADER) + '\n')
        base_results = results[ALGO_SET[0]]
        custom_results = results[ALGO_SET[1]]
        base_ratio_sum = 0
        custom_ratio_sum = 0
        for task in results[ALGO_SET[0]].keys():
            size = base_results[task][2]
            base_iterations = base_results[task][1]
            custom_iterations = custom_results[task][1]
            number_of_solutions = math_factorial(size)

            base_ratio = base_iterations / number_of_solutions - 1
            custom_ratio = custom_iterations / number_of_solutions - 1

            base_ratio_sum += base_ratio
            custom_ratio_sum += custom_ratio

            _file.write(','.join(map(str, [size, base_iterations, str(base_ratio)[:FLOAT_LENGTH],
                custom_iterations, str(custom_ratio)[:FLOAT_LENGTH], '\n'])))

        base_ratio_avg = base_ratio_sum / len(results[ALGO_SET[0]])
        custom_ratio_avg = custom_ratio_sum / len(results[ALGO_SET[0]])
        _file.write(','.join(map(str, ['', '', base_ratio_avg, '', custom_ratio_avg])))

def main():
    args = parse_arguments()
    files = os_listdir(args.tasks)
    assert(len(files) > 0)

    results = {}
    for algo in ALGO_SET:
        results[algo] = {}
        for file in files:
            process = subprocess.run(f"{args.binary} {args.tasks}/{file} {algo}", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            parsed_result = parse_output(process.stdout) + (TASK_SIZE_PATTERN.search(file).group(1),)
            results[algo][file] = parsed_result

if __name__ == "__main__":
    main()
