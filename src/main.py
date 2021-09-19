from problems.n_puzzle.n_puzzle_problem import NPuzzleProblem
from problems.n_puzzle.n_puzzle_state import NPuzzleState

from problems.route_finding.location import Location
from problems.route_finding.route_finding import RouteFinding
from solvers import BFS, DFS, BestFirstSearch, AStar, IDAStar
from solvers.utils import Heap
import numpy as np


from problems.n_puzzle import NPuzzleProblem
from problems.n_puzzle import NPuzzleState

def main_routefinding():
    a = Location("A", (0, 0))
    b = Location("B", (1, 1))
    c = Location("C", (2, 0))
    d = Location("D", (1, -1))
    
    pr = RouteFinding([a, b, c, d], [(a, b, 10), (b, c, 1), (a, d, 1), (d, c, 9)], a, c)

    bfs = BFS(pr, pr.initial)
    target_bfs = bfs.run()
    print(f"BFS: {target_bfs.path()}")

    dfs = DFS(pr, pr.initial)
    target_dfs = dfs.run()
    print(f"DFS: {target_dfs.path()}")

    bestfs= BestFirstSearch(pr, pr.initial)
    target_bestfs = bestfs.run()
    print(f"bestfirst: {target_bestfs.path()}")

    dist = lambda s: np.linalg.norm(np.array(s.coord) - np.array(pr.goal.coord), ord=np.inf)
    astar= AStar(pr, pr.initial, dist)
    target_astar = astar.run()
    print(f"astar: {target_astar.path()}")

    idastar= IDAStar(pr, pr.initial)
    target_idastar = idastar.run(dist)
    print(f"idastar: {target_idastar.path()}")





def main_n_puzzle():
    start_matrix = [[2, 8, 3],
                    [1, 6, 4],
                    [7, 0, 5]]

    final_matrix = [[1, 2, 3],
                    [8, 0, 4],
                    [7, 6, 5]]

    start_state = NPuzzleState(start_matrix, 2, 1)
    final_state = NPuzzleState(final_matrix, 1, 1)

    """
    start_matrix = [[3, 1, 2],
                    [0, 4, 5],
                    [6, 7, 8]]

    final_matrix = [[3, 1, 2],
                    [6, 4, 5],
                    [7, 0, 8]]

    start_state = NPuzzleState(start_matrix, 1, 0)
    final_state = NPuzzleState(final_matrix, 2, 0)
    """
    
    p = NPuzzleProblem(start_state, final_state)

    solver = DFS(p, start_state)
    target_solver = solver.run()
    print(f"SOLVER:: {target_solver.path()}")

def main_heap():
    class node:
        def __init__(self, value, cost):
            self.value = value
            self.cost = cost

        def __str__(self):
            return f"{self.value} {self.cost}"

        def __repr__(self):
            return self.__str__()

    nodes = [node(i, np.random.randint(0, 10)) for i in range(10)]

    h = Heap(nodes, maxheap=True, key=lambda x: x.cost)
    print(h.elements)
    h.put(node("11", 120))
    print(h.elements)
    print(h.get())




if __name__ == '__main__':
    main_n_puzzle()
    #main_routefinding()