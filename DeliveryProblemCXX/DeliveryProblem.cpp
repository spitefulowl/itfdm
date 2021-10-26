// DeliveryProblem.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//

#include <iostream>
#include "BranchAndBounds.h"

int main(int argc, char* argv[])
{
	Task task(argv[1]);
	//Task task("../Task2/task_2_07_n15.txt");
	BaseLowerBound lower_bound(task);
	BaseUpperBound upper_bound(task);
	BranchAndBound algorithm(task);

	BreadthFirstTraversal traversal{};
	auto&& result = algorithm.solve(traversal, lower_bound, upper_bound);
	std::cout << "Iterations: " << result.second << std::endl;
	std::cout << "Solution: ";
	for (auto& elem : result.first) {
		std::cout << elem << " ";
	}
	std::cout << std::endl;
	std::cout << "Crit: " << get_crit(task, result.first) << std::endl;
	return 0;
}
