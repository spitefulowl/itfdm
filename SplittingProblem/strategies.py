from random import shuffle as random_shuffle
from random import random as random
from math import floor as math_floor

class BaseOneStepStrat():
    def __init__(self, workpiece_lengths):
        self.workpiece_lengths = workpiece_lengths

    def get(self, permutation):
        return sorted(permutation, key=lambda x: self.workpiece_lengths[x], reverse=True)

class CustomOneStepStrat():
    def __init__(self, workpiece_lengths):
        self.workpiece_lengths = workpiece_lengths

    def get(self, permutation):
        sorted_permutaion = BaseOneStepStrat(self.workpiece_lengths).get(permutation)
        result_permutation = []
        print(permutation)

        while len(sorted_permutaion) > 0:
            median = sorted_permutaion.pop(math_floor(len(sorted_permutaion) / 2))
            result_permutation.append(median)

            if len(sorted_permutaion) > 0:
                result_permutation.append(sorted_permutaion.pop())

        assert(len(result_permutation) == len(permutation))
        return list(reversed(result_permutation))

class BaseMultiStepStrat():
    def __init__(self):
        pass

    def get(self, permutation, _):
        result_permutation = permutation.copy()
        random_shuffle(result_permutation)
        return result_permutation

class CustomMultiStepStrat():
    def __init__(self, workpiece_lengths):
        self.workpiece_lengths = workpiece_lengths

    def get(self, permutation, solution):
        if not solution:
            return permutation

        result_permutation = []
        sorted_solution = sorted(solution, key=lambda x: len(x), reverse=True)

        split_idx = math_floor(len(sorted_solution) / 2)
        small_wp_rods = sorted_solution[:split_idx]
        large_wp_rods = sorted_solution[split_idx:]

        for idx, small_wps in enumerate(small_wp_rods):
            result_permutation.extend(large_wp_rods[idx] + small_wps)
        if len(sorted_solution) % 2 != 0:
            result_permutation.extend(large_wp_rods[-1])

        result_permutation = CustomOneStepStrat(self.workpiece_lengths).get(result_permutation)
        # print(result_permutation)
        assert(len(result_permutation) == len(permutation))
        return result_permutation
