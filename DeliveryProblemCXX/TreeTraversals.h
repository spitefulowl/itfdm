#pragma once
#include "Task.h"
#include <list>

class Traversal {
public:
	virtual Vertex get(std::list<Vertex>& vertices) = 0;
};

class BreadthFirstTraversal : public Traversal {
	virtual Vertex get(std::list<Vertex>& vertices) override {
		if (vertices.size() == 0) {
			return Vertex{};
		}
		auto result = vertices.front();
		vertices.pop_front();
		return result;
	}
};
