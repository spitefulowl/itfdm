#include "bounds.h"

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
	if (additional_destination == 0) this->my_cache[key] = current_crit;
	return current_crit;
}

CustomUpperBound::CustomUpperBound(Task& task) : my_task(task), my_base_bound(BaseUpperBound(task)) {
	this->my_cache.set_empty_key(0);
}

std::size_t CustomUpperBound::get(Vertex& vertex, std::size_t additional_destination, bool save_result) {
	std::size_t key = vertex.get_id();
	if (this->my_cache.find(key) != this->my_cache.end() && additional_destination == 0 && save_result == false) {
		return this->my_cache[key];
	}
	std::size_t base_crit = this->my_base_bound.get(vertex, additional_destination);
	Vertex* vertex_copy = nullptr;
	if (save_result) {
		vertex_copy = new Vertex(vertex);
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

	std::size_t descendant_prev = 0;
	if (base_size && additional_destination == 0) {
		descendant_prev = vertex[base_size - 1];
	}
	else {
		descendant_prev = additional_destination;
	}

	for (std::size_t idx = 0; idx < task_size - base_size; ++idx) {
		std::size_t min_time = INT_MAX;
		std::size_t min_descendant = 0;
		for (std::size_t possible_descendant = 0; possible_descendant < task_size; ++possible_descendant) {
			if (descendants_mask & (1llu << possible_descendant)) {
				std::size_t time = this->my_task.get_delivery_time(descendant_prev, possible_descendant + 1);
				if (min_time > time) {
					min_time = time;
					min_descendant = possible_descendant;
				}
			}
		}
		current_time += min_time;
		descendant_prev = min_descendant + 1;
		descendants_mask ^= 1llu << min_descendant;
		if (this->my_task.get_target_date(min_descendant) < current_time) {
			++current_crit;
		}
		if (save_result) {
			vertex.push_back(min_descendant + 1);
		}

	}
	if (base_crit < current_crit) {
		current_crit = base_crit;
		if (save_result) {
			this->my_base_bound.get(*vertex_copy, additional_destination, true);
			vertex = *vertex_copy;
		}
	}
	if (additional_destination == 0) this->my_cache[key] = current_crit;
	return current_crit;
}

BaseLowerBound::BaseLowerBound(Task& task, bool disable_cache) : my_task(task) {
	this->disable_cache = disable_cache;
	this->my_cache.set_empty_key(0);
}

std::size_t BaseLowerBound::get(Vertex& vertex, std::size_t additional_destination) {
	if (additional_destination != 0) vertex.push_back(additional_destination);
	std::size_t key = vertex.get_id();
	if (this->my_cache.find(key) != this->my_cache.end() && additional_destination == 0 && !disable_cache) {
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
	else if (!disable_cache) {
		this->my_cache[key] = current_crit;
	}
	return current_crit;
}

CustomLowerBound::CustomLowerBound(Task& task) : my_task(task), my_base_bound(BaseLowerBound(task, true)) {
	this->my_cache.set_empty_key(0);
}

std::size_t CustomLowerBound::get(Vertex& vertex, std::size_t additional_destination) {
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

	std::size_t prev_vertex_idx = vertex[base_size - 1];

	std::size_t min_time = INT_MAX;
	for (std::size_t idx = 0; idx < task_size - base_size; ++idx) {
		std::size_t min_target_date = INT_MAX;
		std::size_t min_vertex_idx = 0;
		for (std::size_t possible_descendant = 0; possible_descendant < task_size; ++possible_descendant) {
			std::size_t time = this->my_task.get_delivery_time(prev_vertex_idx, possible_descendant + 1);
			if (time < min_time && prev_vertex_idx != possible_descendant + 1) {
				min_time = time;
			}
			if (descendants_mask & (1llu << possible_descendant)) {
				std::size_t current_date = this->my_task.get_target_date(possible_descendant);
				if (min_target_date > current_date && min_time + current_time <= current_date) {
					min_target_date = current_date;
					min_vertex_idx = possible_descendant;
				}
			}
		}
		if (min_target_date == INT_MAX) {
			current_crit += task_size - base_size - idx;
			break;
		}
		prev_vertex_idx = min_vertex_idx + 1;
		current_time += min_time;
		descendants_mask ^= 1llu << min_vertex_idx;
		if (min_target_date < current_time) {
			current_crit += 1;
		}
	}

	std::size_t base_crit = this->my_base_bound.get(vertex);
	if (base_crit > current_crit) {
		current_crit = base_crit;
	}

	if (additional_destination != 0) {
		vertex.pop_back();
	}
	else {
		this->my_cache[key] = current_crit;
	}
	return current_crit;
}
