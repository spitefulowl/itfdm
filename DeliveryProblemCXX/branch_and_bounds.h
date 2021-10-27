#pragma once

#include "tree_traversals.h"
#include "bounds.h"
#include <deque>

class BranchAndBound {
public:
	BranchAndBound(Task& task) : my_task(task) {}

	std::pair<Vertex, std::size_t> solve(Traversal& strategy, LowerBound& lower_bound, UpperBound& upper_bound) {
		std::list<Vertex> current_vertices{};
		std::size_t iterations = 0;

		while (true) {
			if (current_vertices.size() == 1) {
				auto&& solution = current_vertices.front();
				auto&& current_lower_bound_result = lower_bound.get(solution);
				auto&& current_upper_bound_result = upper_bound.get(solution);
				std::size_t test = get_crit(this->my_task, solution);
				if (current_lower_bound_result == current_upper_bound_result) {
					current_upper_bound_result = upper_bound.get(solution, 0, true);
					return std::make_pair(solution, iterations);
				}
			}

			Vertex current_vertex = std::move(strategy.get(current_vertices));
			iterations += check_vertices(current_vertices, current_vertex, lower_bound, upper_bound);
		}
	}

private:
	std::size_t check_vertices(std::list<Vertex>& current_vertices, Vertex& current_vertex, LowerBound& lower_bound, UpperBound& upper_bound) {
		std::size_t my_iterations = 0;
		std::size_t task_size = this->my_task.size();
		std::size_t descendants_mask = get_descendants_mask(current_vertex);
		std::size_t min_uppper_bound_dest_idx = 0;
		for (std::size_t possible_descendant = 0; possible_descendant < task_size; ++possible_descendant) {
			if (descendants_mask & (1llu << possible_descendant)) {
				++my_iterations;
				std::size_t current_upper_bound = upper_bound.get(current_vertex, possible_descendant + 1);
				if (current_upper_bound <= min_upper_bound) {
					min_uppper_bound_dest_idx = possible_descendant + 1;
					min_upper_bound = current_upper_bound;
				}
			}
		}

		if (min_uppper_bound_dest_idx != 0) {
			auto& remove_begin = std::remove_if(current_vertices.begin(), current_vertices.end(), [&](auto& elem) {
				auto lower = lower_bound.get(elem);
				return lower >= min_upper_bound;
			});
			current_vertices.erase(remove_begin, current_vertices.end());
		}
		for (std::size_t possible_descendant = 0; possible_descendant < task_size; ++possible_descendant) {
			if (descendants_mask & (1llu << possible_descendant)) {
				auto lower_bound_res = lower_bound.get(current_vertex, possible_descendant + 1);
				if (lower_bound_res < min_upper_bound || min_uppper_bound_dest_idx == possible_descendant + 1) {
					Vertex new_vertex = current_vertex;
					new_vertex.push_back(possible_descendant + 1);
					current_vertices.push_back(std::move(new_vertex));
				}
			}
		}
		return my_iterations;
	}

	std::size_t min_upper_bound = INT_MAX;
	Task& my_task;
};