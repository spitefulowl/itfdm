#include <iostream>
#include "branch_and_bounds.h"

int main(int argc, char* argv[])
{
	Task task(argv[1]);
	//Task task("../Task2/task_2_09_n50.txt");
	//if (std::strcmp(argv[2], "base") == 0) {
	if (std::strcmp("base", "base") == 0) {
		CustomLowerBound lower_bound(task);
		CustomUpperBound upper_bound(task);
		BranchAndBound algorithm(task);

		//BreadthFirstTraversal traversal{};
		CustomTraversal traversal(lower_bound, upper_bound, task.size());
		auto&& result = algorithm.solve(traversal, lower_bound, upper_bound);
		std::cout << "Iterations: " << result.second << std::endl;
		std::cout << "Solution: ";
		for (auto& elem : result.first) {
			std::cout << elem << " ";
		}
		std::cout << std::endl;
		std::cout << "Crit: " << get_crit(task, result.first) << std::endl;
	}
	return 0;
}
