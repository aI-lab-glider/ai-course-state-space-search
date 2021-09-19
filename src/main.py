from problems.route_finding.location import Location
from problems.route_finding.route_finding import RouteFinding
from solvers import BFS, DFS, BestFirstSearch, AStar, IDAStar
from solvers.utils import Heap
import numpy as np


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
    # print(nodes)

    h = Heap(nodes, maxheap=True, key=lambda x: x.cost)
    print(h.elements)
    h.put(node("11", 120))
    print(h.elements)
    print(h.get())


if __name__ == '__main__':
    main_routefinding()


    

