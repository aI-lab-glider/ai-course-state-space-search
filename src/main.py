from benchmark import Benchmark
from problems.n_puzzle.n_puzzle_problem import NPuzzleProblem
from problems.n_puzzle.n_puzzle_state import NPuzzleState
from problems.n_puzzle.n_puzzle_heuristic import NPuzzleHeuristic

from problems.route_finding.location import Location
from problems.route_finding.route_finding import RouteFinding
from problems.route_finding.heuristic import RouteFindingHeuristic

from problems.rush_hour.vehicle import RushHourVehicle, Orientation
from problems.rush_hour.rush_hour import RushHourProblem
from problems.rush_hour.board import RushHourBoard
from problems.rush_hour.blocking_cars_heuristic import BlockingCarsHeuristic
from problems.rush_hour.distance_to_exit_heuristic import DistanceToExitHeuristic

from solvers import BFS, DFS, BestFirstSearch, AStar, IDAStar
import numpy as np


def main_routefinding():
    a = Location("A", (0, 0))
    b = Location("B", (1, 1))
    c = Location("C", (2, 0))
    d = Location("D", (1, -1))
    
    pr = RouteFinding([a, b, c, d], [(a, b, 10), (b, c, 1), (a, d, 1), (d, c, 9)], a, c)
    RFheuristic = RouteFindingHeuristic(pr).apply

    bfs = BFS(pr, pr.initial)
    target_bfs = bfs.run()
    print(f"BFS: {target_bfs.path()}")
    
    dfs = DFS(pr, pr.initial)
    target_dfs = dfs.run()
    print(f"DFS: {target_dfs.path()}")

    bestfs= BestFirstSearch(pr, pr.initial)
    target_bestfs = bestfs.run()
    print(f"bestfirst: {target_bestfs.path()}")

    astar= AStar(pr, pr.initial, RFheuristic)
    target_astar = astar.run()
    print(f"astar: {target_astar.path()}")

    idastar= IDAStar(pr, pr.initial)
    target_idastar = idastar.run(RFheuristic)
    print(f"idastar: {target_idastar.path()}")


def main_n_puzzle():
    start_matrix = [[2, 8, 3],
                    [1, 6, 4],
                    [0, 7, 5]]

    final_matrix = [[1, 2, 3],
                    [8, 0, 4],
                    [7, 6, 5]]

    start_state = NPuzzleState(start_matrix, 2, 0)
    final_state = NPuzzleState(final_matrix, 1, 1)

    p = NPuzzleProblem(start_state, final_state)
    NPheuristic = NPuzzleHeuristic(p).apply

    solver = BFS(p, start_state)
    target_solver = solver.run()
    print(f"Solver: {target_solver.path()}")

    astar= AStar(p, start_state, NPheuristic)
    target_astar = astar.run()
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
    heuristic = NPuzzleHeuristic(p).apply

    b = Benchmark(p)
    b.compare((["BFS", "BestFirstSearch", "AStar", "DFS"], heuristic))
    b.print_grades()


def main_rush_hour():
    x = RushHourVehicle('X', 3, 2, Orientation.HORIZONTAL)
    a = RushHourVehicle('A', 0, 0, Orientation.HORIZONTAL)
    b = RushHourVehicle('B', 2, 0, Orientation.HORIZONTAL)
    c = RushHourVehicle('C', 4, 0, Orientation.VERTICAL)
    d = RushHourVehicle('D', 0, 1, Orientation.VERTICAL)  
    e = RushHourVehicle('E', 2, 1, Orientation.HORIZONTAL)
    f = RushHourVehicle('F', 1, 2, Orientation.VERTICAL)
    g = RushHourVehicle('G', 0, 5, Orientation.HORIZONTAL)
    o = RushHourVehicle('O', 5, 0, Orientation.VERTICAL) 
    p = RushHourVehicle('P', 2, 2, Orientation.VERTICAL)
    q = RushHourVehicle('Q', 3, 3, Orientation.HORIZONTAL) 

    vehicles = {x, a, b, c, d, e, f, g, o, p, q}
    board = RushHourBoard(vehicles) 
    problem = RushHourProblem(vehicles, board)
    BCHeuristic = BlockingCarsHeuristic().apply
    DTEHeuristic = DistanceToExitHeuristic().apply

    solver = BFS(problem, board)
    target_bfs = solver.run()
    print(f"Solver: {target_bfs.path()}") 

    dfs = DFS(problem, board)
    target_dfs = dfs.run()
    print(f"DFS: {target_dfs.path()}")

    bestfs= BestFirstSearch(problem, board)
    target_bestfs = bestfs.run()
    print(f"bestfirst: {target_bestfs.path()}")

    astar= AStar(problem, board, BCHeuristic)
    target_astar = astar.run()
    print(f"astar: {target_astar.path()}")

    # idastar= IDAStar(problem, board)
    # target_idastar = idastar.run(DTEHeuristic)
    # print(f"idastar: {target_idastar.path()}")

if __name__ == '__main__':
    # main_n_puzzle()
    # main_routefinding()
    #main_benchmark()
    main_rush_hour()