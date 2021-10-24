from delivery_task import DeliveryTask
from utils import get_descendants
from utils import get_crit
from utils import get_time

class BaseLowerBound():
    def __init__(self, task: DeliveryTask):
        self.task = task
        self._my_cache = {}

    def get(self, vertex):
        if self._my_cache.get(vertex):
            return self._my_cache.get(vertex)
        current_crit = get_crit(self.task, vertex)
        current_time = get_time(self.task, vertex)
        descendants = get_descendants(self.task.size, vertex)

        for possible_descendant in descendants:
            if current_time + self.task.delivery_matrix[vertex[-1], possible_descendant] > self.task.target_dates[possible_descendant - 1]:
                current_crit += 1

        self._my_cache[vertex] = current_crit
        return current_crit
