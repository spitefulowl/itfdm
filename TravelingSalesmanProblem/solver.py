import numpy as np

from clustering import base_get_clusters
from salesman_task import SalesmanTask

import utils

class Solver():
    def __init__(self, task: SalesmanTask, clusters_count, depth, clusters_get_callable=base_get_clusters):
        self.clusters_count = clusters_count
        self.depth = depth
        self.task = task
        self._clusters_get_callable = clusters_get_callable
        self._cluster_points = np.array([point for point in range(clusters_count)])

    def set_clusters_getter(self, clusters_get_callable):
        self._clusters_get_callable = clusters_get_callable

    def _restore_solution(self, cluster_solution, solutions):
        solution = []
        for cluster_idx in cluster_solution[:-1]:
            pass

    def _recursive_solve(self, points, current_depth):
        if current_depth == 0:
            return utils.greedy_solve(self.task.distances, points)

        centers = []
        solutions = []
        clusters = self._clusters_get_callable(points, self.task.distances, self.clusters_count)
        for cluster in clusters.values():
            centers.append(cluster.mean(axis=0))
            if len(clusters) < self.clusters_count:
                solutions.append(utils.greedy_solve(self.task.distances, cluster))
            else:
                solutions.append(self._recursive_solve(cluster, current_depth - 1))

        centers = np.array(centers)
        centers_distances = utils.compute_distances(centers)
        cluster_solution = utils.bruteforce_solve(centers_distances, self._cluster_points)
        return self._restore_solution(cluster_solution, solutions)

    def solve(self):
        points = [point for point in range(len(self.task.distances))]
        return self._recursive_solve(points, self.depth)
