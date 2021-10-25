#pragma once
#include <cstddef>
#include <vector>
#include <string>

using Vertex = std::vector<std::size_t>;

class Task {
public:
	Task(std::string filename);
	const std::size_t& get_target_date(std::size_t order);
	const std::size_t& get_delivery_time(std::size_t from, std::size_t to);
	const std::size_t& size();

private:
	std::size_t my_size;
	std::vector<std::size_t> target_dates;
	std::vector<std::size_t> delivery_matrix;
};
