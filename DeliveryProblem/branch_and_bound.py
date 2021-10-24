from utils import get_descendants

min_upper_bound = 9999999
min_upper_bound_updated = False
min_upper_bound_item = None

class BranchAndBound():
    @staticmethod
    def _check_vertices(current_vertices, current_vertex, descendants, lower_bound, upper_bound):
        global min_upper_bound
        global min_upper_bound_updated
        global min_upper_bound_item
        min_upper_bound_updated = False
        for descendant in descendants:
            current_new_vertex = current_vertex + (descendant,)
            current_upper_bound = upper_bound.get(current_new_vertex)[0]
            if current_upper_bound <= min_upper_bound:
                min_upper_bound = current_upper_bound
                min_upper_bound_item = current_new_vertex
                min_upper_bound_updated = True

        if min_upper_bound_updated:
            to_drop = []
            for vertex in current_vertices:
                if lower_bound.get(vertex) >= min_upper_bound and min_upper_bound_item != vertex:
                    to_drop.append(vertex)

            for item in to_drop:
                current_vertices.remove(item)

        for descendant in descendants:
            current_new_vertex = current_vertex + (descendant,)
            if lower_bound.get(current_new_vertex) < min_upper_bound or min_upper_bound_item == current_new_vertex:
                current_vertices.add(current_new_vertex)

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
            current_vertices.discard(current_vertex)
            descendants = get_descendants(size, current_vertex)
            BranchAndBound._check_vertices(current_vertices, current_vertex, descendants, lower_bound, upper_bound)
            iterations += 1

        return solution, iterations
