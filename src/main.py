
from benchmark import Benchmark

from problems.blocks_world.blocks_world_heuristic import BlocksWorldHeuristic
from problems.blocks_world.blocks_world_problem import BlocksWorldProblem
from problems.blocks_world.blocks_world_state import BlocksWorldState

from problems.n_puzzle.n_puzzle_problem import NPuzzleProblem
from problems.n_puzzle.n_puzzle_state import NPuzzleState
from problems.n_puzzle.n_puzzle_manhattan_heuristic import NPuzzleManhattanHeuristic
from problems.n_puzzle.n_puzzle_euclidean_heuristic import NPuzzleEuclideanHeuristic

from problems.route_finding.location import Location
from problems.route_finding.route_finding import RouteFinding
from problems.route_finding.manhattan_heuristic import RouteFindingManhattanHeuristic
from problems.route_finding.euclidean_heuristic import RouteFindingEuclideanHeuristic
from problems.route_finding.diagonal_heuristic import RouteFindingDiagonalHeuristic

from problems.rush_hour.vehicle import RushHourVehicle, Orientation
from problems.rush_hour.rush_hour import RushHourProblem
from problems.rush_hour.board import RushHourBoard
from problems.rush_hour.blocking_cars_heuristic import BlockingCarsHeuristic
from problems.rush_hour.distance_to_exit_heuristic import DistanceToExitHeuristic

from solvers import BFS, DFS, Dijkstra, Greedy, AStar, IDAStar
import numpy as np


def main_routefinding():
    a = Location("A", (0, 0))
    b = Location("B", (1, 1))
    c = Location("C", (2, 0))
    d = Location("D", (1, -1))
    
    pr = RouteFinding([a, b, c, d], [(a, b, 10), (b, c, 1), (a, d, 1), (d, c, 9)], a, c)
    RFMHeuristic = RouteFindingManhattanHeuristic(pr)
    RFEHeuristic = RouteFindingEuclideanHeuristic(pr)
    RFDHeuristic = RouteFindingDiagonalHeuristic(pr)

    bfs = BFS(pr)
    target_bfs = bfs.solve()
    print(f"BFS: {target_bfs.path()}")
    
    dfs = DFS(pr)
    target_dfs = dfs.solve()
    print(f"DFS: {target_dfs.path()}")

    bestfs= Dijkstra(pr)
    target_bestfs = bestfs.solve()
    print(f"bestfirst: {target_bestfs.path()}")

    astar= AStar(pr, pr.initial, RFMHeuristic)
    target_astar = astar.solve()
    print(f"astar: {target_astar.path()}")

    # idastar= IDAStar(pr, pr.initial)
    # target_idastar = idastar.run(RFMHeuristic)
    # print(f"idastar: {target_idastar.path()}")

    # b = Benchmark(pr)
    # b.compare((["BFS", "BestFirstSearch", "AStar", "DFS"], RFEHeuristic))
    # b.print_grades()

def main_n_puzzle():
    with open("problems/n_puzzle/instances/03_06.txt") as f:
        text = f.read()
        p = NPuzzleProblem.deserialize(text)
    NPMHeuristic = NPuzzleManhattanHeuristic(p)
    NPEHeuristic = NPuzzleEuclideanHeuristic(p)

    solver = BFS(p)
    target_solver = solver.solve()
    print(f"Solver: {target_solver.path()}")

    astar= AStar(p, NPEHeuristic)
    target_astar = astar.solve()
    print(f"astar: {target_astar.path()}")

def main_benchmark():
    start_matrix = [[2, 8, 3],
                    [1, 6, 4],
                    [0, 7, 5]]

    final_matrix = [[1, 2, 3],
                    [8, 0, 4],
                    [7, 6, 5]]

    start_state = NPuzzleState(start_matrix, 2, 0)
    final_state = NPuzzleState(final_matrix, 1, 1)

    p = NPuzzleProblem(start_state, final_state)
    MHeuristic = NPuzzleManhattanHeuristic(p)
    EHeuristic = NPuzzleEuclideanHeuristic(p)

    b = Benchmark(p)
    b.compare([(["BFS", "BestFirstSearch", "AStar", "DFS"], MHeuristic)])
    b.print_grades()


def main_rush_hour():
    with open("problems/rush_hour/instances/hardest.txt") as f:
        text = f.read()
        problem = RushHourProblem.deserialize(text)

    BCHeuristic = BlockingCarsHeuristic(problem)
    DTEHeuristic = DistanceToExitHeuristic(problem)

    # solver = BFS(problem)
    # target_bfs = solver.solve()
    # print(f"Solver: {target_bfs.path()}") 

    # dfs = DFS(problem)
    # target_dfs = dfs.solve()
    # print(f"DFS: {target_dfs.path()}")

    bestfs = Dijkstra(problem)
    target_bestfs = bestfs.solve()
    print(f"bestfirst: {target_bestfs.path()}")

    # astar= AStar(problem, BCHeuristic)
    # target_astar = astar.solve()
    # print(f"astar: {target_astar.path()}")

    # idastar= IDAStar(problem, BCHeuristic)
    # target_idastar = idastar.solve()
    # print(f"idastar: {target_idastar.path()}")

    # b = Benchmark(problem)
    # b.compare((["BFS", "BestFirstSearch", "AStar", "DFS"], BCHeuristic))
    # b.print_grades()    

def main_blocks_world():
    with open("problems/blocks_world/instances/03_07_14.txt") as f:
        text = f.read()
        problem = BlocksWorldProblem.deserialize(text)
    heuristic = BlocksWorldHeuristic(problem)

    astar = IDAStar(problem, heuristic)
    target_astar = astar.solve()
    print(f"astar: {target_astar.path()}")

if __name__ == '__main__':
    # main_n_puzzle()
    # main_routefinding()
    # main_benchmark()
    main_rush_hour()
    # main_blocks_world()
    
