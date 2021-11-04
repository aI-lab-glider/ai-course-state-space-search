
import argparse
import re

from typing import Dict, Optional, Type, Union, Set, cast
from base.problem import Problem
from base.heuristic import Heuristic
from base.solver import HeuristicSolver, Solver
from problems.blocks_world.blocks_world_heuristic import BlocksWorldNaiveHeuristic
from problems.blocks_world.blocks_world_problem import BlocksWorldProblem

from problems.n_puzzle.n_puzzle_problem import NPuzzleProblem
from problems.n_puzzle.heuristics.n_puzzle_manhattan_heuristic import NPuzzleManhattanHeuristic
from problems.n_puzzle.heuristics.n_puzzle_euclidean_heuristic import NPuzzleEuclideanHeuristic

from problems.grid_pathfinding.grid_pathfinding import GridPathfinding
from problems.grid_pathfinding.heuristics.manhattan_heuristic import GridManhattanHeuristic
from problems.grid_pathfinding.heuristics.euclidean_heuristic import GridEuclideanHeuristic
from problems.grid_pathfinding.heuristics.diagonal_heuristic import GridDiagonalHeuristic
from problems.rush_hour.rush_hour import RushHourProblem
from problems.rush_hour.heuristics.blocking_cars_heuristic import RushHourBlockingCarsHeuristic
from problems.rush_hour.heuristics.distance_to_exit_heuristic import RushHourDistanceToExitHeuristic

from solvers import BFS, DFS, Dijkstra, Greedy, AStar, IDAStar, IDDFS
from tree.node import Node

from pathlib import Path
from tree.tree import NodeEvent, NodeEventSubscriber, Tree
import time

VERSION = "0.42 — Lazy Leviathan"

class SolvingMonitor(NodeEventSubscriber, Solver):
    def __init__(self, solver: Solver, instance: Union[str, Path]) -> None:
        super().__init__(solver.problem)
        if isinstance(instance, Path):
            self.instance = instance.stem
        else:
            self.instance = Path(instance).stem
        self.solver = solver
        self.solver.search_tree().subscribe(self)
        self._reset_stats()
    
    def solve(self) -> Optional[Node]:
        self._reset_stats()
        self.print_header()
        result = self.solver.solve()
        self.print_footer(result)
        return result

    def search_tree(self) -> Tree:
        return self.solver.search_tree()
    
    def _reset_stats(self):
        self.start_time = time.time()
        self.closed_nodes = 0
        self.opened_nodes = 1
        self.wall_time = 0

    def got_event(self, node: Node, event: NodeEvent) -> None:
        if event == NodeEvent.Closed:
            self.closed_nodes += 1
            self.opened_nodes -= 1
        elif event == NodeEvent.Opened:
            self.opened_nodes += 1
        self.wall_time = time.time() - self.start_time
        self.print_stats()
    
    def print_header(self):
        header = f"----------------- State Search Solver ------------------\n"\
                 f"----------- version: {VERSION} -------------\n"\
                 f"-------- @ 2021 Summer Project at Glider|AI Lab --------\n"\
                 f"--------------------------------------------------------\n"\
                 f".....problem:  {self._problem_name()}\n"\
                 f"....instance:  {self.instance}\n"\
                 f"...algorithm:  {self._solver_name()}"
        heuristic = self._heuristic_name()
        if heuristic is not None:
            header += f"\n...heuristic:  {heuristic}"
        header += f"\n____________________| SEARCH STATS |____________________"
        print(header)

    def _solver_name(self) -> str:
        return self.solver.__class__.__name__
    
    def _problem_name(self) -> str:
        return self.solver.problem.__class__.__name__

    def _heuristic_name(self) -> Optional[str]:
        if isinstance(self.solver, HeuristicSolver):
            return self.solver.heuristic.__class__.__name__
        else:
            return None

    def print_footer(self, result: Optional[Node]):
        print("\n--------------------------------------------------------")
        if result is None:
            print("\n...failed to solve :(\n...either the problem is unsolvable or there is a bug in the solver")
            return 

        img_name = f"{self._problem_name()}_{self.instance}_{self._solver_name()}"
        heuristic = self._heuristic_name()
        if heuristic is not None:
            img_name += f"_{heuristic}"
        img_name += ".gif"

        imgs = []
        path_limit = 1000
        if len(result.path()) < path_limit:
            for node in result.path():
                imgs.append(self.solver.problem.to_image(node.state))
            imgs[0].save(img_name, save_all=True, append_images=imgs[1:], format='GIF', optimize=False, duration=500, loop=1)
        else:
            print(f'resulted path is too big ({path_limit} + nodes), so skiping saving its visualization, to avoid memomry issues')
        print(f"...solved succesfully!")
        print(f"...solution cost: {result.cost}")
        print(f"...visual output: {img_name}")

    def print_stats(self):
        print(f"\r| open: {self.opened_nodes:<9} | closed: {self.closed_nodes:<9} | time: {self.wall_time:<8.2f} |", end='', flush=True)


def snake_to_camel(snake: str) -> str:
    return ''.join(x.title() for x in snake.split('_'))


def camel_to_snake(camel: str, useless_suffix: str = '') -> str:
    useful_camel = camel.removesuffix(useless_suffix)
    return re.sub(r'(?<!^)(?=[A-Z])', '_', useful_camel).lower()


problem_heuristics: Dict[type[Problem], Set[type[Heuristic]]] = {
    GridPathfinding : {GridEuclideanHeuristic, GridDiagonalHeuristic, GridManhattanHeuristic},
    NPuzzleProblem : {NPuzzleEuclideanHeuristic, NPuzzleManhattanHeuristic},
    RushHourProblem : {RushHourDistanceToExitHeuristic, RushHourBlockingCarsHeuristic},
    BlocksWorldProblem : {BlocksWorldNaiveHeuristic}
}

avl_problems : Dict[str, type[Problem]] = { camel_to_snake(p.__name__, "Problem") : cast(type[Problem], p)
                 for p in
                 [GridPathfinding, NPuzzleProblem, RushHourProblem, BlocksWorldProblem]}

avl_algos : Dict[str, type[Solver]] = { a.__name__.lower() : cast(type[Solver], a) for a in [DFS, BFS, Dijkstra, Greedy, AStar, IDAStar, IDDFS]}

all_heuristics : Set[type[Heuristic]] = set.union(*problem_heuristics.values())
avl_heuristics : Dict[str, type[Heuristic]] = { camel_to_snake(h.__name__, "Heuristic") : cast(type[Heuristic], h) 
                   for h in all_heuristics }

def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("instance", help="path to the problem instance to be solved")
    parser.add_argument("-p", "--problem", required=True, choices=avl_problems.keys(), help="name of the problem type corresponding to the given instance")
    parser.add_argument("-a", "--algorithm", required=True, choices=avl_algos.keys(), help="name of the algorithm solver should use")
    parser.add_argument("-h", "--heuristic", choices=avl_heuristics.keys(), help="name of the heuristic that should be used by the solver")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    instance = args.instance
    problem_class = avl_problems[args.problem]
    algorithm_class = avl_algos[args.algorithm]

    try:
        with open(instance) as instance_file:
            instance_text = instance_file.read()
            problem = problem_class.deserialize(instance_text)
    except FileNotFoundError as e:
        print("> Path to the instance seems to be incorrect, are you sure of it?")
        exit(-1)
    except Exception as e:
        print("> Failed to load the instance, are you sure, you've chosen correct problem type?")
        exit(-1)

    algorithm : Optional[Solver] = None
    if issubclass(algorithm_class, HeuristicSolver):
        if not args.heuristic:
            print("> Chosen algorithm requires a heuristic, please specify it!")
            exit(-1)

        heuristic_class = avl_heuristics[args.heuristic]

        if heuristic_class not in problem_heuristics[problem_class]:
            print("> Chosen heuristic doesn't apply to the given problem. Choose another!")
            print("> Lifehack: names of heuristics and related problems are pretty similar :)")
            exit(-1)
        
        algorithm = algorithm_class(problem, heuristic_class(problem))
    else:
        algorithm = algorithm_class(problem)
    
    assert algorithm is not None
    solver_monitor = SolvingMonitor(algorithm, instance)
    solver_monitor.solve()

        

    
    
        
        
    


    
