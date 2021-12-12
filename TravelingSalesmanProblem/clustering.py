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

    for k, v in clusters.items():
        clusters[k] = np.array(v)

    return clusters

def _base_find_cluster_points(points, distances, start_points: list, clusters_count: int):
    for iter_idx in range(clusters_count - len(start_points)):
        start_points.append(_get_far_point(points, distances, start_points))

    return start_points

def base_get_clusters(points, distances, clusters_count, task=None):
    start_points = list(max(combinations(points, 2), key=lambda x: distances[x[0]][x[1]]))
    cluster_points = _base_find_cluster_points(points, distances, start_points, clusters_count)
    clusters = _base_find_clusters(points, distances, cluster_points)
    return clusters

def custom_get_clusters(points, distances, clusters_count, task=None):
    assert(clusters_count % 2 == 0)
    if len(points) != len(distances):
        return base_get_clusters(points, distances, clusters_count)

    min_x = task.points[points[0]][0]
    max_x = task.points[points[0]][0]
    min_y = task.points[points[0]][1]
    max_y = task.points[points[0]][1]
    for point in points:
        point_x, point_y = task.points[point]
        if point_x < min_x:
            min_x = point_x - 1
        if max_x < point_x:
            max_x = point_x + 1
        if point_y < min_y:
            min_y = point_y - 1
        if max_y < point_y:
            max_y = point_y + 1

    x_num_groups = (clusters_count / 2)
    y_num_groups = 2

    x_step = (max_x - min_x) / x_num_groups
    y_step = (max_y - min_y) / y_num_groups

    clusters = { idx: [] for idx in range(clusters_count) }
    for point in points:
        x, y = task.points[point]
        x_group = int((x - min_x) / x_step)
        y_group = int((y - min_y) / y_step)
        if x_group == int(clusters_count / 2):
            x_group -= 1
        if y_group == 2:
            y_group -= 1

        cluster_idx = x_num_groups * y_group + x_group
        clusters[cluster_idx].append(point)

    clusters = { k: v for k, v in clusters.items() if v }
    for k, v in clusters.items():
        clusters[k] = np.array(v)

    return clusters
