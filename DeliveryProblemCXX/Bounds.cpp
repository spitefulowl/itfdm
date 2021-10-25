#include "Bounds.h"

BaseUpperBound::BaseUpperBound(Task& task) : my_task(task) { }

solution BaseUpperBound::get(Vertex& vertex, std::size_t additional_destination) {
	if (additional_destination != 0) vertex.push_back(additional_destination);
	std::size_t descendants_mask = get_descendants_mask(vertex);
	std::size_t base_size = vertex.size();
	std::size_t task_size = this->my_task.size();
	std::vector<std::size_t> current_solution = vertex;

	if (base_size == task_size) {
		if (additional_destination != 0) vertex.pop_back();
		return std::make_pair(vertex, get_crit(this->my_task, vertex));
	}

	std::size_t current_time = get_time(this->my_task, vertex);

	for (std::size_t idx = 0; idx < task_size - base_size; ++idx) {
		std::size_t current_size = current_solution.size();
		std::size_t min_time_diff = INT_MAX;
		std::size_t min_time = INT_MAX;
		std::size_t min_descendant = 0;
		std::size_t time_diff = 0;

		for (std::size_t possible_descendant = 0; possible_descendant < task_size; ++possible_descendant) {
			if (descendants_mask & (1 << possible_descendant)) {
				std::size_t current_time_tmp = current_time + this->my_task.get_delivery_time(current_size - 1, possible_descendant + 1);
				if (current_time_tmp <= this->my_task.get_target_date(possible_descendant)) {
					time_diff = this->my_task.get_target_date(possible_descendant) - current_time_tmp;
				}
				else {
					time_diff = INT_MAX;
				}

				if (min_time_diff > time_diff) {
					min_time_diff = time_diff;
					min_time = current_time_tmp;
					min_descendant = possible_descendant;
				}
			}
		}

		if (min_time_diff != INT_MAX) {
			current_solution.push_back(min_descendant + 1);
			current_time += min_time;
			descendants_mask ^= 1 << min_descendant;
		}
		else {
			insert_by_mask(current_solution, descendants_mask, task_size);
			std::size_t crit = get_crit(this->my_task, current_solution);
			if (additional_destination != 0) vertex.pop_back();
			return std::make_pair(std::move(current_solution), crit);
		}
	}
	std::size_t crit = get_crit(this->my_task, current_solution);
	if (additional_destination != 0) vertex.pop_back();
	return std::make_pair(std::move(current_solution), crit);
}

BaseLowerBound::BaseLowerBound(Task& task) : my_task(task) { }

std::size_t BaseLowerBound::get(Vertex& vertex, std::size_t additional_destination) {
	if (additional_destination != 0) vertex.push_back(additional_destination);
	std::size_t current_crit = get_crit(this->my_task, vertex);
	std::size_t current_time = get_time(this->my_task, vertex);
	std::size_t descendants_mask = get_descendants_mask(vertex);
	std::size_t task_size = this->my_task.size();
	std::size_t base_size = vertex.size();

	for (std::size_t possible_descendant = 0; possible_descendant < task_size; ++possible_descendant) {
		if (descendants_mask & (1 << possible_descendant)) {
			if (current_time + this->my_task.get_delivery_time(vertex[base_size - 1], possible_descendant + 1) > this->my_task.get_target_date(possible_descendant)) {
				current_crit += 1;
			}
		}
	}

	if (additional_destination != 0) vertex.pop_back();
	return current_crit;
}
