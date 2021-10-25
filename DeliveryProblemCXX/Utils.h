#pragma once
#include <vector>
#include "Task.h"

inline std::size_t get_descendants_mask(std::vector<std::size_t>& vertex) {
	std::size_t mask = static_cast<std::size_t>(-1);
	for (auto&& elem : vertex) {
		mask ^= 1 << (elem - 1);
	}
	return mask;
}

inline std::size_t get_time(Task& task, Vertex& vertex) {
	std::size_t time = task.get_delivery_time(0, vertex[0]);
	for (std::size_t idx = 1; idx < vertex.size(); ++idx) {
		time += task.get_delivery_time(vertex[idx - 1], vertex[idx]);
	}
	return time;
}

inline std::size_t get_crit(Task& task, Vertex& vertex, std::size_t additional_destination = 0) {
	std::size_t result = 0;
	std::size_t time = task.get_delivery_time(0, vertex[0]);
	if (time > task.get_target_date(vertex[0] - 1)) ++result;

	for (std::size_t idx = 1; idx < vertex.size(); ++idx) {
		time += task.get_delivery_time(vertex[idx - 1], vertex[idx]);
		if (time > task.get_target_date(vertex[idx] - 1)) {
			result += 1;
		}
	}

	if (additional_destination != 0) {
		time += task.get_delivery_time(vertex[vertex.size() - 1], additional_destination);
		if (time > task.get_target_date(additional_destination - 1)) {
			result += 1;
		}
	}

	return result;
}

inline void insert_by_mask(std::vector<std::size_t>& my_vector, std::size_t mask, std::size_t size) {
	for (std::size_t idx = 0; idx < size; ++idx) {
		if (mask & 1 << idx) {
			my_vector.push_back(idx + 1);
		}
	}
}
