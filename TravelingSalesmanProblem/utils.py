import numpy as np
import scipy.spatial

import itertools
import random

from itertools import product

def get_crit(distances, solution):
    result = 0
    current_point = solution[0]
    for point in solution[1:]:
        result += float(distances[current_point][point])
        current_point = point

    return result + float(distances[current_point][solution[0]])

def greedy_solve(distances, points):
    if len(points) == 1:
        return points

    points_list = points.tolist()
    solution = [points_list.pop()]
    while points_list:
        nearest_point = points_list[0]
        min_distance = distances[solution[-1]][nearest_point]
        for point in points_list:
            distance = distances[solution[-1]][point]
            if distance < min_distance:
                min_distance = distance
                nearest_point = point

        points_list.remove(nearest_point)
        solution.append(nearest_point)

    return np.array(solution)

def bruteforce_solve(distances, points):
    return np.array(min(itertools.permutations(points), key=lambda x: get_crit(distances, x)))

def compute_distances(points):
    if len(np.asmatrix(points)) == 1:
        return np.array([0])

    return np.array([scipy.spatial.distance.cdist(points, np.asmatrix(point)).flatten('C')
                        for point in points])

def base_selector(next_solution, solution, task):
    nearest_pair = min(product([solution[-1]], next_solution), key=lambda x: task.distances[x[0]][x[1]])
    split_point_idx = np.where(next_solution==nearest_pair[1])[0][0]
    if random.randint(0, 1):
        return next_solution[split_point_idx:].tolist() + next_solution[:split_point_idx].tolist()
    else:
        return list(reversed(next_solution.tolist()))[split_point_idx:] + list(reversed(next_solution.tolist()))[:split_point_idx]
