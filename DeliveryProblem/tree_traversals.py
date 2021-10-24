class BreadthFirst():
    def __init__(self):
        pass

    def get(self, current_vertices):
        if not current_vertices:
            return tuple()
        # if len(current_vertices) == 1:
        #     print('FATAL: not solution')
        #     exit(-1)

        return min(current_vertices, key=lambda x: len(x))
