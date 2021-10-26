#pragma once
#include "task.h"
#include <deque>

class Traversal {
public:
	virtual Vertex get(std::deque<Vertex>& vertices) = 0;
};

class BreadthFirstTraversal : public Traversal {
	virtual Vertex get(std::deque<Vertex>& vertices) override {
		if (vertices.size() == 0) {
			Vertex my_vertex{};
			my_vertex.reserve(15);
			return std::move(my_vertex);
		}
		Vertex result = std::move(vertices.front());
		vertices.pop_front();
		return std::move(result);
	}
};
