from utils import get_descendants

class BranchAndBound():
    @staticmethod
    def check_vertices(current_vertices, lower_bound, upper_bound):
        min_upper_bound = upper_bound.task.size
        for item in current_vertices:
            current_upper_bound = upper_bound.get(item)[0]
            if current_upper_bound <= min_upper_bound:
                min_upper_bound = current_upper_bound
                min_upper_bound_item = item

        to_drop = []
        for vertex in current_vertices:
            if lower_bound.get(vertex) >= min_upper_bound and min_upper_bound_item != vertex:
                to_drop.append(vertex)

        for item in to_drop:
            current_vertices.remove(item)

    @staticmethod
    def solve(size, strategy, lower_bound, upper_bound):
        current_vertices = set()
        current_lower_bound = 0
        current_upper_bound = size
        iterations = 0
        while True:
            if len(current_vertices) == 1:
                solution = current_vertices.pop()
                current_lower_bound = lower_bound.get(solution)
                current_upper_bound = upper_bound.get(solution)
                if current_lower_bound == current_upper_bound[0]:
                    solution = current_upper_bound[1]
                    break

            current_vertex = strategy.get(current_vertices)
            current_vertices -= set([current_vertex])
            descendants = get_descendants(size, current_vertex)
            current_vertices.update([current_vertex + (descendant,) for descendant in descendants])
            BranchAndBound.check_vertices(current_vertices, lower_bound, upper_bound)
            iterations += 1

        return solution, iterations
