// DeliveryProblem.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//

#include <iostream>
#include "Task.h"
#include "Bounds.h"

int main(int argc, char* argv[])
{
	Task task("Task2/task_2_01_n3.txt");
	BaseUpperBound bound(task);
	std::vector<std::size_t> my_vector = { 3 };
	auto result = bound.get(my_vector);
	for (auto& elem : result.first) {
		std::cout << elem << " ";
	}
	std::cout << std::endl;
	std::cout << result.second << std::endl;
	return 0;
}
