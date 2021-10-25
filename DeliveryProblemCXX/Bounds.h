#pragma once

#include <utility>
#include <vector>
#include <unordered_map>
#include "Task.h"
#include "Utils.h"

using solution = std::pair<std::vector<std::size_t>, std::size_t>;

class UpperBound {
public:
	virtual solution get(Vertex& vertex, std::size_t additional_destination = 0) = 0;
};

class LowerBound {
public:
	virtual std::size_t get(Vertex& vertex, std::size_t additional_destination = 0) = 0;
};

class BaseUpperBound : public UpperBound {
public:
	BaseUpperBound(Task& task);
	virtual solution get(Vertex& vertex, std::size_t additional_destination = 0) override;
private:
	Task& my_task;
	std::unordered_map<std::string, solution> my_cache{};
};

class BaseLowerBound : public LowerBound {
public:
	BaseLowerBound(Task& task);
	virtual std::size_t get(Vertex& vertex, std::size_t additional_destination = 0) override;
private:
	Task& my_task;
	std::unordered_map<std::string, std::size_t> my_cache{};
};
