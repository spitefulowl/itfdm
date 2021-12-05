import numpy as np
import scipy.spatial

import itertools

def get_crit(distances, solution):
    result = 0
    current_point = solution[0]
    for point in solution[1:]:
        result += distances[current_point][point]
        current_point = point

    return result + distances[current_point][solution[0]]

def greedy_solve(distances, points):
    points_list = points.to_list()
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
    return np.array(min(itertools.permutations(points), key=lambda x: get_crit(x)))

def compute_distances(points):
    return np.array([scipy.spatial.distance.cdist(points, np.asmatrix(point))
                        for point in points])
