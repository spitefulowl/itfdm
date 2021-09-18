from random import shuffle as random_shuffle

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
