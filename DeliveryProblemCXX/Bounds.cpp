#include "Bounds.h"

BaseUpperBound::BaseUpperBound(Task& task) : my_task(task) {
	this->my_cache.set_empty_key(0);
}

std::size_t BaseUpperBound::get(Vertex& vertex, std::size_t additional_destination, bool save_result) {
	std::size_t key = vertex.get_id();
	if (this->my_cache.find(key) != this->my_cache.end() && additional_destination == 0 && save_result == false) {
		return this->my_cache[key];
	}

	std::size_t base_size = vertex.size();
	std::size_t task_size = this->my_task.size();

	if (base_size == task_size) {
		return get_crit(this->my_task, vertex);
	}

	std::size_t descendants_mask = get_descendants_mask(vertex);
	if (additional_destination) {
		descendants_mask ^= 1llu << (additional_destination - 1);
		++base_size;
		if (save_result) {
			vertex.push_back(additional_destination);
			additional_destination = 0;
		}
	}

	std::size_t current_crit = get_crit(this->my_task, vertex, additional_destination);
	std::size_t current_time = get_time(this->my_task, vertex, additional_destination);

	std::size_t min_descendant_prev = 0;
	if (base_size && additional_destination == 0) {
		min_descendant_prev = vertex[base_size - 1];
	}
	else {
		min_descendant_prev = additional_destination;
	}

	for (std::size_t idx = 0; idx < task_size - base_size; ++idx) {
		std::size_t min_time_diff = INT_MAX;
		std::size_t min_time = INT_MAX;
		std::size_t time_diff = 0;
		std::size_t min_descendant = 0;

		for (std::size_t possible_descendant = 0; possible_descendant < task_size; ++possible_descendant) {
			if (descendants_mask & (1llu << possible_descendant)) {
				std::size_t current_time_tmp = current_time + this->my_task.get_delivery_time(min_descendant_prev, possible_descendant + 1);
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
			current_time = min_time;
			descendants_mask ^= 1llu << min_descendant;
			min_descendant_prev = min_descendant + 1;
			if (save_result) {
				vertex.push_back(min_descendant_prev);
			}
		}
		else {
			for (std::size_t possible_descendant = 0; possible_descendant < task_size; ++possible_descendant) {
				if (descendants_mask & (1llu << possible_descendant)) {
					++current_crit;
					if (save_result) {
						vertex.push_back(possible_descendant + 1);
					}
				}
			}
			if (additional_destination == 0) {
				this->my_cache[key] = current_crit;
			}
			return current_crit;
		}
	}
	this->my_cache[key] = current_crit;
	return current_crit;
}

BaseLowerBound::BaseLowerBound(Task& task) : my_task(task) {
	this->my_cache.set_empty_key(0);
}

std::size_t BaseLowerBound::get(Vertex& vertex, std::size_t additional_destination) {
	if (additional_destination != 0) vertex.push_back(additional_destination);
	std::size_t key = vertex.get_id();
	if (this->my_cache.find(key) != this->my_cache.end() && additional_destination == 0) {
		return this->my_cache[key];
	}

	std::size_t current_crit = get_crit(this->my_task, vertex);
	std::size_t current_time = get_time(this->my_task, vertex);
	std::size_t descendants_mask = get_descendants_mask(vertex);
	std::size_t task_size = this->my_task.size();
	std::size_t base_size = vertex.size();

	for (std::size_t possible_descendant = 0; possible_descendant < task_size; ++possible_descendant) {
		if (descendants_mask & (1llu << possible_descendant)) {
			if (current_time + this->my_task.get_delivery_time(vertex[base_size - 1], possible_descendant + 1) > this->my_task.get_target_date(possible_descendant)) {
				current_crit += 1;
			}
		}
	}

	if (additional_destination != 0) {
		vertex.pop_back();
	}
	else {
		//this->my_cache[key] = current_crit;
	}
	return current_crit;
}
