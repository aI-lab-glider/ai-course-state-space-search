from solvers import AStar, IDAStar, BestFirstSearch, BFS, DFS
from base import Problem
from typing import List, Callable, Sequence, Tuple
from timeit import default_timer


# Sprawdzanie ilości wywołań kolejek fifo/lifo
class Benchmark:
    def __init__(self, problem: Problem):
        self.problem = problem


    def compare(self, adj_list: Sequence[Tuple[List[str], Callable]] = None):
        if adj_list:
            for algo in adj_list[0]:
                self.run_algorithm(algo, adj_list[1])
        return None


    """
    TODO
    AStar przyjmuje heurystykę w definicji problemu
    IDAStar przyjmuje heurystyke przy wywołaniu metody run()
    Zamieniłbym, żeby IDAStar przyjmował heurystykę w definicji problemu.
    """
    def run_algorithm(self, algo: str, dist: Callable = None):
        solver = {
            "BFS": BFS(self.problem, self.problem.initial),
            "DFS": DFS(self.problem, self.problem.initial),
            "BestFirstSearch": BestFirstSearch(self.problem, self.problem.initial),
            "AStar": AStar(self.problem, self.problem.initial, dist)
            # "IDAStar": IDAStar(self.problem, self.problem.initial) 
        }[algo]

        start = default_timer()
        data = solver.run()
        stop = default_timer()

        time = round(stop - start, 5)
        self.grades.append((algo, time))

        return None

    
    def print_grades(self):
        for grade in self.grades:
            print(f"Alg: {grade[0]} --> Time: {grade[1]}")

