from typing import Any, Callable, List, Optional
from base.heuristic import Heuristic, NoHeuristic
from base.problem import Problem
from base.state import State
from solvers.utils import PriorityQueue
from tree.node import Node
from tree.tree import Tree


class SearchProcess:
    def __init__(self, problem: Problem,
                 start_state: State, goal_state: State,
                 eval_fun: Callable[[Node], float], heuristic: Heuristic = NoHeuristic()):
        self.start_state, self.goal_state = start_state, goal_state
        self.problem = problem
        self.eval_fun = eval_fun
        self.tree = Tree(Node(start_state))
        self._visited = {self.start_state: self.tree.root.cost}
        self.frontier = PriorityQueue(eval_fun, [self.tree.root])
        self.heuristic = heuristic
        self.solution_node = self.tree.root

    @property
    def path(self) -> List[Node]:
        return self.solution_node.path()

    def expand_frontier(self, upper_bound_cost: float, opposite_process: 'SearchProcess'):
        """
        Solves tree in one direction.
        """
        candidate_found = True
        while candidate_found:
            candidates = self._find_candidates(upper_bound_cost)
            candidate = self._select_candidate(candidates, upper_bound_cost,
                                               opposite_process)
            candidate_found = candidate is not None
            if candidate is not None:
                candidate_found = True
                if not opposite_process.has_visited_state(candidate.state):
                    for node in self.tree.expand(self.problem, candidate):
                        if self.state_cost(node.state) > node.cost:
                            self._visited[node.state] = node.cost
                            self.solution_node = node
                            self.frontier.push(node)
                            upper_bound_cost = min(upper_bound_cost, self.state_cost(node.state)
                                                   + opposite_process.state_cost(node.state))
        return upper_bound_cost

    def state_cost(self, state: State):
        return self._visited.get(state, float('inf'))

    def has_visited_state(self, state: State):
        return state in self._visited

    def _find_candidates(self, upper_bound_cost) -> PriorityQueue:
        candidates = PriorityQueue(self.eval_fun)
        while not self.frontier.is_empty():
            candidate = self.frontier.pop()
            for node in self.tree.expand(self.problem, candidate):
                if self.eval_fun(node) - self.heuristic(self.goal_state) < upper_bound_cost:
                    candidates.push(node)
        return candidates

    def _select_candidate(self, candidates: PriorityQueue[Node], upper_bound_cost: float,
                          opposite_process: 'SearchProcess') -> Optional[Node]:
        candidate = None
        while candidates and not candidate:
            candidate = candidates.pop()
            cost_through_state = self.state_cost(
                candidate.state) + opposite_process.state_cost(candidate.state)
            if not opposite_process.has_visited_state(candidate.state) and cost_through_state >= upper_bound_cost:
                continue
            else:
                break
        return candidate

    def can_expand_frontier(self):
        return not self.frontier.is_empty()


class BidirectionalSearch:

    def __init__(self, problem: Problem[State, Any], eval_fun: Callable[[Node], float],
                 heuristic: Heuristic = NoHeuristic()):
        self.problem = problem
        self.forward_process = SearchProcess(problem,
                                             problem.initial, problem.goal,
                                             eval_fun, heuristic)
        self.backward_process = SearchProcess(problem,
                                              problem.goal, problem.initial,
                                              eval_fun, heuristic)

    @property
    def search_tree(self):
        return self.forward_process.tree

    def solve(self):
        upper_bound_cost = float('inf')
        while self.forward_process.can_expand_frontier() and self.backward_process.can_expand_frontier():
            upper_bound_cost = self.forward_process.expand_frontier(
                upper_bound_cost, self.backward_process)
            upper_bound_cost = self.backward_process.expand_frontier(
                upper_bound_cost, self.forward_process)

        self.backward_process.path[0].parent = self.forward_process.path[-1]
        return self.backward_process.path[-1]
