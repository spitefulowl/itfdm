#pragma once
#include "task.h"
#include "bounds.h"
#include <list>

class Traversal {
public:
	virtual Vertex get(std::list<Vertex>& vertices) = 0;
};

class BreadthFirstTraversal : public Traversal {
public:
	virtual Vertex get(std::list<Vertex>& vertices) override {
		if (vertices.size() == 0) {
			return std::move(Vertex{});
		}
		Vertex result = std::move(vertices.front());
		vertices.pop_front();
		return std::move(result);
	}
};

class CustomTraversal : public Traversal {
public:
	CustomTraversal(LowerBound& lower_bound, UpperBound& upper_bound, std::size_t max_size) : lower_bound(lower_bound), upper_bound(upper_bound), max_size(max_size) {}
	virtual Vertex get(std::list<Vertex>& vertices) override {
		if (vertices.size() == 0) {
			return std::move(Vertex{});
		}
		auto cur_iter = vertices.begin();
		auto best_iter = vertices.begin();
		double ratio = 0;
		for (; cur_iter != vertices.end(); ++cur_iter) {
			if (cur_iter->size() == this->max_size) {
				continue;
			}
			double current_ratio = ((double)this->lower_bound.get(*cur_iter) / (double)this->upper_bound.get(*cur_iter));
			if (current_ratio > ratio) {
				ratio = current_ratio;
				best_iter = cur_iter;
			}
		}
		Vertex result = std::move(*best_iter);
		vertices.erase(best_iter);
		return std::move(result);
	}
private:
	LowerBound& lower_bound;
	UpperBound& upper_bound;
	std::size_t max_size;
};
