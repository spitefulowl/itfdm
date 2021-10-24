from delivery_task import DeliveryTask
from utils import get_descendants
from utils import get_time
from utils import get_crit

INT_MAX = 999999999

class BaseUpperBound():
    def __init__(self, task: DeliveryTask):
        self.task = task

    def get(self, vertex):
        descendants = get_descendants(self.task.size, vertex)
        base_size = len(vertex)
        current_solution = vertex

        crit = self.task.size
        currrent_time = get_time(self.task, vertex)

        for idx in range(self.task.size - base_size):
            current_size = len(current_solution)
            min_time_diff = INT_MAX
            min_time = INT_MAX
            min_descendant = None

            for possible_descendant in descendants:
                current_time_tmp = currrent_time + self.task.delivery_matrix[current_size - 1, possible_descendant]
                if current_time_tmp <= self.task.target_dates[possible_descendant - 1]:
                    time_diff = self.task.target_dates[possible_descendant - 1] - current_time_tmp
                else:
                    time_diff = INT_MAX

                if min_time_diff > time_diff:
                    min_time_diff = time_diff
                    min_time = current_time_tmp
                    min_descendant = possible_descendant

            if min_time_diff != INT_MAX:
                current_solution += (min_descendant,)
                currrent_time += min_time
                descendants.remove(min_descendant)
                crit = self.task.size - len(current_solution)
            else:
                current_solution += tuple(descendants)
                return (get_crit(self.task, current_solution), current_solution)

        return (crit, current_solution)
