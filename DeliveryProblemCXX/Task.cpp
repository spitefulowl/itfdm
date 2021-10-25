#include "Task.h"
#include <fstream>
#include <sstream>

Task::Task(std::string filename) {
	std::fstream file = std::fstream(filename, std::ios::in);
	if (file.fail()) {
		std::printf("FATAL: File %s not found\n", filename.c_str());
		std::exit(-1);
	}
	std::string current_line;
	std::getline(file, current_line);
	this->my_size = std::stoi(current_line);
	current_line.clear();

	std::getline(file, current_line);
	std::stringstream stream(current_line);

	for (std::size_t idx = 0; idx < this->my_size; ++idx) {
		std::size_t value{};
		stream >> value;
		this->target_dates.push_back(value);
	}

	for (std::size_t idx1 = 0; idx1 < this->my_size + 1; ++idx1) {
		std::getline(file, current_line);
		std::stringstream stream(current_line);
		std::size_t value{};
		for (std::size_t idx2 = 0; idx2 < this->my_size + 1; ++idx2) {
			stream >> value;
			delivery_matrix.push_back(value);
		}
	}
}

const std::size_t& Task::get_target_date(std::size_t order) {
	return this->target_dates[order];
}

const std::size_t& Task::get_delivery_time(std::size_t from, std::size_t to) {
	return this->delivery_matrix[from * (this->my_size + 1) + to];
}

const std::size_t& Task::size() {
	return this->my_size;
}
