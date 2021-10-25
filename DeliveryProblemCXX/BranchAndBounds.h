#pragma once

#include "TreeTraversals.h"
#include "Bounds.h"

class BranchAndBound {
public:
	BranchAndBound(Task& task) : my_task(task) {}

	solution solve(Traversal& strategy, LowerBound& lower_bound, UpperBound& upper_bound) {
		std::list<Vertex> current_vertices{};
		std::size_t current_lower_bound = 0;
		std::size_t current_upper_bound = this->my_task.size();
		std::size_t iterations = 0;

		while (true) {
			if (current_vertices.size() == 1) {
				auto&& solution = current_vertices.front();
				auto&& current_lower_bound = lower_bound.get(solution);
				auto&& current_upper_bound = upper_bound.get(solution);
				if (current_lower_bound == current_upper_bound.second) {
					return std::make_pair(current_upper_bound.first, iterations);
				}
			}

			Vertex current_vertex = std::move(strategy.get(current_vertices));
			check_vertices(current_vertices, current_vertex, lower_bound, upper_bound);
			++iterations;
		}
	}

private:
	void check_vertices(std::list<Vertex>& current_vertices, Vertex& current_vertex, LowerBound& lower_bound, UpperBound& upper_bound) {
		Vertex* min_upper_bound_item = nullptr;
		std::size_t task_size = this->my_task.size();
		std::size_t descendants_mask = get_descendants_mask(current_vertex);
		std::size_t min_uppper_bound_dest_idx = 0;
		for (std::size_t possible_descendant = 0; possible_descendant < task_size; ++possible_descendant) {
			if (descendants_mask & (1llu << possible_descendant)) {
				std::size_t current_upper_bound = upper_bound.get(current_vertex, possible_descendant + 1).second;
				if (current_upper_bound < min_upper_bound) {
					min_uppper_bound_dest_idx = possible_descendant + 1;
					min_upper_bound = current_upper_bound;
				}
			}
		}

		if (min_uppper_bound_dest_idx != 0) {
			auto iter_cur = current_vertices.begin();
			auto iter_end = current_vertices.end();
			while (iter_cur != iter_end) {
				if (lower_bound.get(*iter_cur) >= min_upper_bound) {
					current_vertices.erase(iter_cur++);
					continue;
				}
				++iter_cur;
			}
		}
		for (std::size_t possible_descendant = 0; possible_descendant < task_size; ++possible_descendant) {
			if (descendants_mask & (1llu << possible_descendant)) {
				if (lower_bound.get(current_vertex, possible_descendant + 1) < min_upper_bound || min_uppper_bound_dest_idx == possible_descendant + 1) {
					Vertex new_vertex = current_vertex;
					new_vertex.push_back(possible_descendant + 1);
					current_vertices.push_back(std::move(new_vertex));
				}
			}
		}
	}

	std::size_t min_upper_bound = INT_MAX;
	Task& my_task;
};