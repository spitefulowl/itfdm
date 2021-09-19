from posixpath import split
from random import shuffle as random_shuffle
from math import floor as math_floor

class BaseOneStepStrat():
    def __init__(self, workpiece_lengths):
        self.workpiece_lengths = workpiece_lengths

    def get(self, permutation):
        return sorted(permutation, key=lambda x: self.workpiece_lengths[x], reverse=True)

class BaseMultiStepStrat():
    def __init__(self):
        pass

    def get(self, permutation):
        result_permutation = permutation.copy()
        random_shuffle(result_permutation)
        return result_permutation

class CustomOneStepStrat():
    def __init__(self, workpiece_lengths):
        self.workpiece_lengths = workpiece_lengths

    def get(self, permutation):
        sorted_permutaion = BaseOneStepStrat(self.workpiece_lengths).get(permutation)
        result_permutation = []

        while len(sorted_permutaion) > 0:
            median = sorted_permutaion.pop(math_floor(len(sorted_permutaion) / 2))
            result_permutation.append(median)

            if len(sorted_permutaion) > 0:
                result_permutation.append(sorted_permutaion.pop())

        assert(len(result_permutation) == len(permutation))
        return list(reversed(result_permutation))
