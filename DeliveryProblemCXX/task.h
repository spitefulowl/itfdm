#pragma once
#include <cstddef>
#include <vector>
#include <string>

static std::size_t vertex_id = 0;

static std::size_t init_vertex_id() {
	return vertex_id++;
}

class Vertex : public std::vector<std::size_t> {
public:
	using std::vector<std::size_t>::vector;
	Vertex(const Vertex& elem) : std::vector<std::size_t>::vector(elem) {
		my_vertex_idx = init_vertex_id();
	}
	inline std::size_t get_id() {
		return my_vertex_idx;
	}
	inline void update_id() {
		my_vertex_idx = init_vertex_id();
	}
private:
	std::size_t my_vertex_idx = init_vertex_id();
};

class Task {
public:
	Task(std::string filename);
	inline const std::size_t& get_target_date(std::size_t order) { return this->target_dates[order]; }
	inline const std::size_t& get_delivery_time(std::size_t from, std::size_t to) { return this->delivery_matrix[from * (this->my_size + 1) + to]; }
	const std::size_t& size() { return this->my_size; }

private:
	std::size_t my_size;
	std::vector<std::size_t> target_dates;
	std::vector<std::size_t> delivery_matrix;
};
