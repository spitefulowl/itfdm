import unittest
import numpy as np

import utils

class TestUtils(unittest.TestCase):
    def test_greedy_and_exact_solver(self):
        my_points = np.array([[1, 1], [2, 2], [3, 3], [199, 199], [200, 200], [300, 300]])
        my_distances = utils.compute_distances(my_points)
        points = np.array([idx for idx in range(len(my_points))])
        solution_greedy = utils.greedy_solve(my_distances, points)
        np.testing.assert_equal(solution_greedy, np.flip(points))
        solution_exact = utils.bruteforce_solve(my_distances, points)

        crit_greedy = utils.get_crit(my_distances, solution_greedy)
        crit_exact = utils.get_crit(my_distances, solution_exact)
        self.assertLessEqual(crit_exact, crit_greedy)

        for idx in range(10):
            random_points = np.random.random((8, 2))
            random_distances = utils.compute_distances(random_points)
            points = np.array([idx for idx in range(len(random_points))])
            solution_greedy = utils.greedy_solve(random_distances, points)
            solution_exact = utils.bruteforce_solve(random_distances, points)

            print(solution_greedy, solution_exact)
            crit_greedy = utils.get_crit(random_distances, solution_greedy)
            crit_exact = utils.get_crit(random_distances, solution_exact)
            print(crit_greedy, crit_exact)
            self.assertLessEqual(crit_exact, crit_greedy)

if __name__ == '__main__':
    unittest.main()
