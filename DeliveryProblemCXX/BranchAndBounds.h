#pragma once

#include "Bounds.h"

class BranchAndBound {
public:
	BranchAndBound(Task& task) : my_task(task) {}

private:
	void check_vertices(std::list<Vertex>& current_vertices, Vertex& current_vertex, LowerBound& lower_bound, UpperBound& upper_bound) {
		Vertex* min_upper_bound_item = nullptr;
		std::size_t task_size = this->my_task.size();
		std::size_t descendants_mask = get_descendants_mask(current_vertex);
		for (std::size_t possible_descendant = 0; possible_descendant < task_size; ++possible_descendant) {
			if (descendants_mask & (1 << possible_descendant)) {
				/*auto& current_upper_bound = upper_bound.get()*/
			}
		}
	}

	std::size_t min_upper_bound = INT_MAX;
	Task& my_task;
};