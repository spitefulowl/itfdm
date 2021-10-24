from utils import get_descendants

class BranchAndBound():
    @staticmethod
    def check_vertices(current_vertices, lower_bound, upper_bound):
        min_upper_bound = min([upper_bound.get(item)[0] for item in current_vertices])
        for vertex in current_vertices:
            if lower_bound.get(vertex) >= min_upper_bound:
                current_vertices.remove(vertex)

    @staticmethod
    def solve(size, strategy, lower_bound, upper_bound):
        current_vertices = set()
        current_lower_bound = 0
        current_upper_bound = size
        solution = None
        while True:
            if len(current_vertices) == 1:
                current_lower_bound = lower_bound.get(solution)
                current_upper_bound = upper_bound.get(solution)
                if current_lower_bound == current_upper_bound[0]:
                    solution = current_upper_bound[1]
                    break

            current_vertex = strategy.get(current_vertices)
            current_vertices -= set([current_vertex])
            descendants = get_descendants(size, current_vertex)
            current_vertices += set([current_vertex + (descendant,) for descendant in descendants])
            BranchAndBound.check_vertices(current_vertices, lower_bound, upper_bound)

        return solution
