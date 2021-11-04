
import argparse
from cli_config import VERSION, avl_algos, avl_heuristics, avl_problems, problem_heuristics
from typing import Optional, Union
from base.solver import HeuristicSolver, Solver

from tree.node import Node

from pathlib import Path
from tree.tree import NodeEvent, NodeEventSubscriber, Tree
import time

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
        for node in result.path():
            imgs.append(self.solver.problem.to_image(node.state))
        
        imgs[0].save(img_name, save_all=True, append_images=imgs[1:], format='GIF', optimize=True, duration=500, loop=1)
        print(f"...solved succesfully!")
        print(f"...solution cost: {result.cost}")
        print(f"...visual output: {img_name}")

    def print_stats(self):
        print(f"\r| open: {self.opened_nodes:<9} | closed: {self.closed_nodes:<9} | time: {self.wall_time:<8.2f} |", end='', flush=True)



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

        

    
    
        
        
    


    
