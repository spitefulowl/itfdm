import numpy as np

from itertools import combinations
from functools import reduce


def _get_far_point(points, distances, selected_points):
    max_distances_sum = -1
    far_point = -1
    for point in points:
        if point in selected_points:
            continue

        distances_sum = reduce(lambda x, y: x + distances[y][point], selected_points)
        if max_distances_sum < distances_sum:
            max_distances_sum = distances_sum
            far_point = point

    return far_point

def _base_find_clusters(points, distances, cluster_points):
    clusters = { cluster_point: [cluster_point] for cluster_point in cluster_points }
    for point in points:
        if point in cluster_points:
            continue
        nearest_cluster_point = cluster_points[0]
        min_distance = distances[nearest_cluster_point][point]
        for cluster_point in cluster_points:
            distance = distances[cluster_point][point]
            if distance < min_distance:
                min_distance = distance
                nearest_cluster_point = cluster_point

        clusters[nearest_cluster_point].append(point)

    return np.array(clusters)

def _base_find_cluster_points(points, distances, start_points: list, clusters_count: int):
    for point in range(clusters_count - len(start_points)):
        start_points.append(_get_far_point(points, distances, start_points))

    return start_points

def base_get_clusters(points, distances, clusters_count):
    start_points = list(max(combinations(points, 2), key=lambda x: distances[x[0]][x[1]]))
    cluster_points = _base_find_cluster_points(points, distances, start_points, clusters_count)
    clusters = _base_find_clusters(points, distances, cluster_points)
    return clusters
