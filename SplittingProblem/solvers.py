class OneStepSolver():
    def __init__(self, workpiece_lengths, max_rod_length, strategy=None):
        self.workpiece_lengths = workpiece_lengths
        self.max_rod_length = max_rod_length
        self.strategy = strategy
        self._solution = []
        self._rod_lengths = []

    def _find_rod(self, workpiece_number):
        workpiece_length = self.workpiece_lengths[workpiece_number]
        for idx, rod_length in enumerate(self._rod_lengths):
            if rod_length >= workpiece_length:
                self._rod_lengths[idx] -= workpiece_length
                self._solution[idx].append(workpiece_number)
                return

        self._rod_lengths.append(self.max_rod_length - workpiece_length)
        self._solution.append([workpiece_number])

    def solve(self, permutation):
        self._solution.clear()
        self._rod_lengths.clear()
        if self.strategy:
            permutation = self.strategy(permutation, self.workpiece_lengths)
        for workpiece_number in permutation:
            self._find_rod(workpiece_number)

        return self._solution.copy(), len(self._rod_lengths)
