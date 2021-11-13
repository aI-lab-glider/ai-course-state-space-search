import stopit
import argparse
from cli_config import VERSION, avl_algos, avl_problems, problem_heuristics
from typing import Optional, Union
from base.solver import HeuristicSolver, Solver
from tree.node import Node

from pathlib import Path
from tree.tree import NodeEvent, NodeEventSubscriber, Tree
import time


class BenchmarkMonitor(NodeEventSubscriber, Solver):
    def __init__(self, solver: Solver, longest_name: int, timeout: float) -> None:
        super().__init__(solver.problem)
        self.solver = solver
        self.solver.search_tree().subscribe(self)
        self._reset_stats()
        self.longest_name = longest_name
        self.timeout = timeout

    @stopit.threading_timeoutable(default='timeout')
    def solve_with_timeout(self) -> Union[str, Optional[Node]]:
        return self.solver.solve()

    def solve(self) -> Optional[Node]:
        self._reset_stats()
        try:
            result = self.solve_with_timeout(timeout=self.timeout)
        except RecursionError:
            result = "recursion stack overflow"

        self.print_result(result)
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

    def _solver_name(self) -> str:
        return self.solver.__class__.__name__

    def _heuristic_name(self) -> Optional[str]:
        if isinstance(self.solver, HeuristicSolver):
            return self.solver.heuristic.__class__.__name__
        else:
            return None

    def print_stats(self):
        algo_name = self._solver_name()
        heur_name = self._heuristic_name()
        solver_name = f"{algo_name}({heur_name})" if heur_name is not None else algo_name
        print(f"\r{solver_name: >{self.longest_name}} | {self.opened_nodes:<9} | {self.closed_nodes:<9} | {self.wall_time:<8.2f} |", end='', flush=True)

    def print_result(self, result: Union[str, Optional[Node]]):
        if result is None:
            print(" fail")
        elif isinstance(result, str):
            print(f" {result}")
        else:
            print(f" {result.cost}")


def print_header(problem_class, instance, timeout, longest_name):
    print(f"> State Search Benchmark ({VERSION})")
    print(f"-  problem: {problem_class.__name__}")
    print(f"- instance: {Path(instance).stem}")
    print(f"-  timeout: {timeout}s")
    print(f"{'solver name': >{longest_name}} | {'open': <9} | {'closed': <9} | {'time (s)': <8} | result")
    print("-" * 110)


def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "instance", help="path to the problem instance to be solved")
    parser.add_argument("-p", "--problem", required=True, choices=avl_problems.keys(),
                        help="name of the problem type corresponding to the given instance")
    parser.add_argument("-t", "--timeout", type=int, default=30.0,
                        help="how long each algorithm is allowed to work")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    instance = args.instance
    problem_class = avl_problems[args.problem]
    timeout = args.timeout

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

    longest_name = max([len(a.__name__) + len(h.__name__)
                        for a in avl_algos.values()
                        for h in problem_heuristics[problem_class]]) + 2
    print_header(problem_class, instance, timeout, longest_name)
    for algorithm_class in avl_algos.values():
        algorithm: Optional[Solver] = None
        if issubclass(algorithm_class, HeuristicSolver):
            for heuristic_class in problem_heuristics[problem_class]:
                solver_name = f"{algorithm_class.__name__}({heuristic_class.__name__})"
                try:
                    heuristic = heuristic_class(problem)
                    heuristic(problem.initial)
                except NotImplementedError as e:
                    print(
                        f"{solver_name: >{longest_name}} | heuristic is not implemented yet")
                    continue
                except Exception as e:
                    print(
                        f"{solver_name: >{longest_name}} | heuristic raised an error {e}")
                    continue

                try:
                    algorithm = algorithm_class(problem, heuristic)
                    solver_monitor = BenchmarkMonitor(
                        algorithm, longest_name, timeout)
                    solver_monitor.solve()
                except NotImplementedError as e:
                    print(
                        f"{solver_name: >{longest_name}} | algorithm is not implemented yet")
                except Exception as e:
                    print(
                        f"{solver_name: >{longest_name}} | algorithm raised an error {e}")
        else:
            solver_name = algorithm_class.__name__
            try:
                algorithm = algorithm_class(problem)
                solver_monitor = BenchmarkMonitor(
                    algorithm, longest_name, timeout)
                solver_monitor.solve()
            except NotImplementedError as e:
                print(
                    f"{solver_name: >{longest_name}} | algorithm is not implemented yet")
            except Exception as e:
                print(
                    f"{solver_name: >{longest_name}} | algorithm raised an error {e}")
