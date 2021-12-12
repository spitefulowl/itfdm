import unittest
import numpy as np

import clustering
import utils

class TestClustering(unittest.TestCase):
    def test_far_point(self):
        my_points = np.array([[1, 1], [3, 5], [7, 9], [10, 10], [100, 100]])
        my_distances = utils.compute_distances(my_points)
        self.assertEqual(clustering._get_far_point([1, 2, 3], my_distances, [0, 4]), 1)

        my_points = np.array([[1, 1], [3, 5], [7, 9], [10, 10], [100, 100], [1000, 1000]])
        my_distances = utils.compute_distances(my_points)
        self.assertEqual(clustering._get_far_point([1, 2, 3, 5], my_distances, [0, 4]), 5)
        self.assertEqual(clustering._get_far_point([2, 3], my_distances, [0, 4]), 2)

    def test_find_cluster_points(self):
        my_points = np.array([[1, 1], [3, 5], [7, 9], [10, 10], [100, 100]])
        my_distances = utils.compute_distances(my_points)
        expected = { 0: np.array([idx for idx in range(len(my_distances) - 1)]), 4: np.array([4]) }
        result = clustering.base_get_clusters([idx for idx in range(len(my_distances))], my_distances, 2)
        np.testing.assert_equal(result, expected)

        my_points = np.array([[1, 1], [2, 2], [3, 3], [199, 199], [200, 200], [300, 300]])
        my_distances = utils.compute_distances(my_points)
        result = clustering.base_get_clusters([idx for idx in range(len(my_distances))], my_distances, 2)
        expected = { 0: np.array([0, 1, 2]), 5: np.array([5, 3, 4]) }
        np.testing.assert_equal(result, expected)

if __name__ == '__main__':
    unittest.main()
