#pragma once

#include <utility>
#include <vector>
#include <sparsehash/dense_hash_map>
#include "Task.h"
#include "Utils.h"

class UpperBound {
public:
	virtual std::size_t get(Vertex& vertex, std::size_t additional_destination = 0, bool save_result = false) = 0;
};

class LowerBound {
public:
	virtual std::size_t get(Vertex& vertex, std::size_t additional_destination = 0) = 0;
};

class BaseUpperBound : public UpperBound {
public:
	BaseUpperBound(Task& task);
	virtual std::size_t get(Vertex& vertex, std::size_t additional_destination = 0, bool save_result = false) override;
private:
	Task& my_task;
	google::dense_hash_map<std::size_t, std::size_t> my_cache{};
};

class BaseLowerBound : public LowerBound {
public:
	BaseLowerBound(Task& task);
	virtual std::size_t get(Vertex& vertex, std::size_t additional_destination = 0) override;
private:
	Task& my_task;
	google::dense_hash_map<std::size_t, std::size_t> my_cache{};
};
