from solvers import AStar, IDAStar, Dijkstra, Greedy, BFS, DFS
from base import Problem, Heuristic
from typing import List, Callable, Sequence, Tuple
from timeit import default_timer

"""
For now this class compares time only.
"""

class Benchmark:
    def __init__(self, problem: Problem):
        self.problem = problem

        """
        TODO 
        Think about metric system to calculate points and give grade. For now points are just (1000 - 50*time)
        """
        self.points = 1000
        self.grades: List[Tuple[str,float]] = list(tuple())


    def compare(self, adj_list: Sequence[Tuple[List[str], Heuristic]] = None):
        if adj_list:
            for algos, heur in adj_list:
                for algo in algos:
                    self.run_algorithm(algo, heur)
        return None


    """
    TODO
    AStar przyjmuje heurystykę w definicji problemu
    IDAStar przyjmuje heurystyke przy wywołaniu metody solve()
    <Zamieniłbym, żeby IDAStar przyjmował heurystykę w definicji problemu.>
    """
    def run_algorithm(self, algo: str, dist: Heuristic):
        solver = {
            "BFS": BFS(self.problem),
            "DFS": DFS(self.problem),
            "Dijkstra": Dijkstra(self.problem),
            "AStar": AStar(self.problem, dist),
            "IDAStar": IDAStar(self.problem, dist) 
        }[algo]

        start = default_timer()
        solver.solve()
        stop = default_timer()

        time = round(stop - start, 5)
        self.grades.append((algo, time))

        return None

    
    def print_grades(self):
        #TODO
        for grade in self.grades:
            print(f"Alg: {grade[0]} --> Time: {grade[1]} \t| Total: {int(self.points - grade[1]*50)}")

