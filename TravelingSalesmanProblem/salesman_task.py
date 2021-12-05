from re import compile as re_compile

import numpy as np
import scipy.spatial

from utils import compute_distances

class SalesmanTask():
    __coord_pattern = re_compile('\d (\d+.\d+) (\d+.\d+)')

    def __init__(self, filename):
        self._read_task(filename)
        self._compute_distances()

    def _read_task(self, filename):
        with open(filename, 'r') as _file:
            while True:
                if next(_file).strip() == 'NODE_COORD_SECTION':
                    break
            lines = _file.readlines()
            points = []
            for line in lines:
                parsed_line = self.__coord_pattern.search(line)
                if not parsed_line:
                    break
                points.append((float(parsed_line.group(1)), float(parsed_line.group(2))))

            self.points = np.array(points)

    def _compute_distances(self):
        self.distances = compute_distances(self.points)
