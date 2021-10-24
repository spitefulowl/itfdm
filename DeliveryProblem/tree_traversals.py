class BreadthFirst():
    def __init__(self):
        pass

    def get(self, current_vertices):
        return min(current_vertices, key=lambda x: len(x))
