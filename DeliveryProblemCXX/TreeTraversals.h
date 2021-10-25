#pragma once
#include "Task.h"
#include <list>

class Traversal {
public:
	virtual std::size_t get(std::list<std::size_t>& vertices) = 0;
};

class BreadthFirstTraversal : public Traversal {
	virtual std::size_t get(std::list<std::size_t>& vertices) override {
		if (vertices.size() == 0) {
			return static_cast<std::size_t>(-1);
		}
		return vertices.front();
	}
};
