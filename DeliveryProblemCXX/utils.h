#pragma once
#include <vector>
#include <numeric>
#include "task.h"

inline std::size_t get_descendants_mask(std::vector<std::size_t>& vertex) {
	std::size_t mask = static_cast<std::size_t>(-1);
	for (auto&& elem : vertex) {
		mask ^= 1llu << (elem - 1);
	}
	return mask;
}

inline std::size_t get_time(Task& task, Vertex& vertex, std::size_t additional_destination = 0) {
	std::size_t first_vertex = vertex.size() == 0 ? additional_destination : vertex[0];


	std::size_t time = task.get_delivery_time(0, first_vertex);
	for (std::size_t idx = 1; idx < vertex.size(); ++idx) {
		time += task.get_delivery_time(vertex[idx - 1], vertex[idx]);
	}

	if (additional_destination != 0 && vertex.size() != 0) {
		time += task.get_delivery_time(vertex[vertex.size() - 1], additional_destination);
	}

	return time;
}

inline std::size_t get_crit(Task& task, Vertex& vertex, std::size_t additional_destination = 0) {
	std::size_t result = 0;
	std::size_t first_vertex = vertex.size() == 0 ? additional_destination : vertex[0];
	std::size_t time = task.get_delivery_time(0, first_vertex);
	if (time > task.get_target_date(first_vertex - 1)) ++result;

	for (std::size_t idx = 1; idx < vertex.size(); ++idx) {
		time += task.get_delivery_time(vertex[idx - 1], vertex[idx]);
		if (time > task.get_target_date(vertex[idx] - 1)) {
			result += 1;
		}
	}

	if (additional_destination != 0 && vertex.size() != 0) {
		time += task.get_delivery_time(vertex[vertex.size() - 1], additional_destination);
		if (time > task.get_target_date(additional_destination - 1)) {
			result += 1;
		}
	}

	return result;
}

inline void insert_by_mask(std::vector<std::size_t>& my_vector, std::size_t mask, std::size_t size) {
	for (std::size_t idx = 0; idx < size; ++idx) {
		if (mask & 1llu << idx) {
			my_vector.push_back(idx + 1);
		}
	}
}
