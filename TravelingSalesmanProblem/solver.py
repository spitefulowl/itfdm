import numpy as np
from itertools import product
import matplotlib.pyplot as plt

from clustering import base_get_clusters
from salesman_task import SalesmanTask

import utils

class Solver():
    def __init__(self, task: SalesmanTask, clusters_count, depth, get_clusters_callable=base_get_clusters, selector_callable=utils.base_selector):
        self.clusters_count = clusters_count
        self.depth = depth
        self.task = task
        self._get_clusters_callable = get_clusters_callable
        self._selector_callable = selector_callable
        self._cluster_points = np.array([point for point in range(clusters_count)])

    def set_clusters_getter(self, get_clusters_callable):
        self._get_clusters_callable = get_clusters_callable

    def set_selector(self, selector_callable):
        self._selector_callable = selector_callable

    def _restore_solution(self, cluster_solution, solutions):
        solution = []
        current_cluster_idx = cluster_solution[0]
        next_cluster_idx = cluster_solution[1]
        current_solution = solutions[current_cluster_idx]
        next_solution = solutions[next_cluster_idx]
        nearest_pair = min(product(current_solution, next_solution), key=lambda x: self.task.distances[x[0], x[1]])
        start_point_idx = np.where(current_solution==nearest_pair[0])[0][0]
        split_point_idx = np.where(next_solution==nearest_pair[1])[0][0]
        solution += current_solution[start_point_idx:].tolist() + current_solution[:start_point_idx].tolist()
        solution += next_solution[split_point_idx:].tolist() + next_solution[:split_point_idx].tolist()

        for idx in range(2, len(cluster_solution)):
            next_cluster_idx = cluster_solution[idx]
            next_solution = solutions[next_cluster_idx]
            solution += self._selector_callable(next_solution, solution, self.task)

        return np.array(solution)

    def _recursive_solve(self, points, current_depth):
        if current_depth == 0:
            return utils.greedy_solve(self.task.distances, points)

        centers = []
        solutions = []
        clusters = self._get_clusters_callable(points, self.task.distances, self.clusters_count)
        for key, cluster in clusters.items():
            cluster_with_coords = np.array([self.task.points[point] for point in cluster])
            x, y = cluster_with_coords.T
            index = cluster.tolist().index(key)
            # print(f'Cluster: {cluster}')
            # print(f'Center: {key}')
            # print(f'Center coords: {cluster_with_coords[index]}')
            # plt.scatter(x, y)

            centers.append(cluster_with_coords.mean(axis=0))
            if len(cluster) <= self.clusters_count:
                solutions.append(utils.bruteforce_solve(self.task.distances, cluster))
            else:
                solutions.append(self._recursive_solve(cluster, current_depth - 1))

        # plt.show()
        centers = np.array(centers)
        centers_distances = utils.compute_distances(centers)
        cluster_solution = utils.bruteforce_solve(centers_distances, self._cluster_points)
        return self._restore_solution(cluster_solution, solutions)

    def solve(self):
        points = [point for point in range(len(self.task.distances))]
        return self._recursive_solve(points, self.depth)
