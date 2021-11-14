from typing import Any, Callable, Optional
from base.heuristic import Heuristic, NoHeuristic
from base.problem import Problem
from base.state import State
from solvers.utils import PriorityQueue
from tree.node import Node
from tree.tree import NodeEventSubscriber, Tree


class BidirectionalSearchTreeProxy(Tree, NodeEventSubscriber):
    def __init__(self, forward_tree: Tree, backward_tree: Tree):
        self.subscribers = []
        forward_tree.subscribe(self)
        backward_tree.subscribe(self)

    @property
    def root(self):
        raise NotImplementedError(
            "There is no root for the bidirectional tree")

    def got_event(self, node, event):
        self._notify(node, event)


class SearchProcess:
    def __init__(self, problem: Problem,
                 start_state: State, goal_state: State,
                 eval_fun: Callable[[Node], float], heuristic: Heuristic = NoHeuristic()):
        self.start_state, self.goal_state = start_state, goal_state
        self.problem = problem
        self.eval_fun = eval_fun
        self.heuristic = heuristic
        self.tree = Tree(Node(start_state))
        self._visited = {self.tree.root.state: self.tree.root.cost}
        self.frontier = PriorityQueue(eval_fun, [self.tree.root])
        self.meeting_point = self.tree.root

    @property
    def cost_estimate(self):
        """
        Distance to the meeting point based on process'es knowledge.
        """
        return float('inf') if not self.meeting_point else self.eval_fun(self.meeting_point)

    def expand_frontier(self, upper_bound_cost: float, other_process: 'SearchProcess') -> float:
        """
        Makes actual search logic by expanding valid nodes and labeling (assigning cost values) them.

        Args: 
            upper_bound_cost: cost of best path found untill now. Equals to inf, if process, hadn't met before
            other_process: instance that searches tree from the opposite node
        """
        candidates = self._find_candidates(upper_bound_cost)
        candidate = self._select_candidate(
            candidates, upper_bound_cost, other_process)
        if candidate is not None:
            if not other_process.has_visited_state(candidate.state):
                for node in self.tree.expand(self.problem, candidate):
                    if self.state_cost(node.state) > node.cost:
                        upper_bound_cost = self._post_search_phase(
                            node, upper_bound_cost, other_process)
        return upper_bound_cost

    def _find_candidates(self, upper_bound_cost: float) -> PriorityQueue:
        """
        Returns priority queue containing only nodes with smaller estimate value,
        than actual upper bound cost.
        """
        candidates = PriorityQueue(self.eval_fun)
        while self.frontier:
            candidate = self.frontier.pop()
            if self.eval_fun(candidate) - self.heuristic(self.goal_state) < upper_bound_cost:
                candidates.push(candidate)
        return candidates

    def _select_candidate(self, candidates: PriorityQueue[Node], upper_bound_cost: float,
                          other_process: 'SearchProcess') -> Optional[Node]:
        """
        Returns a node, that wasn't visited by another process, or was visited but 
        that path resulted in a higher cost. 
        """
        candidate = None
        while candidates and not candidate:
            candidate = candidates.pop()
            cost_through_state = self.state_cost(
                candidate.state) + other_process.cost_estimate + other_process.heuristic(candidate.state)
            if not other_process.has_visited_state(candidate.state) and cost_through_state >= upper_bound_cost:
                continue
            else:
                break
        return candidate

    def _post_search_phase(self, node: Node, upper_bound_cost: float, other_process: 'SearchProcess') -> float:
        """
        Calculates new upper bound and sets meeting point to node in case, if it promises shorter path.
        """
        new_upper_bound_cost = self._update_stats(
            node, other_process)
        if new_upper_bound_cost < upper_bound_cost:
            upper_bound_cost = new_upper_bound_cost
            self.meeting_point = node
        return new_upper_bound_cost

    def _update_stats(self, node: Node, other_process: 'SearchProcess') -> float:
        """
        Updates statistic used during tree search.
        """
        self._visited[node.state] = node.cost
        self.frontier.push(node)
        upper_bound_cost = self.state_cost(
            node.state) + other_process.state_cost(node.state)
        return upper_bound_cost

    def state_cost(self, state: State):
        return self._visited.get(state, float('inf'))

    def has_visited_state(self, state: State):
        return state in self._visited

    def can_expand_frontier(self):
        return not self.frontier.is_empty()


class BidirectionalSearch:

    def __init__(self, problem: Problem[State, Any], eval_fun: Callable[[Node], float],
                 heuristic: Heuristic = NoHeuristic()):
        self.problem = problem
        self.forward_search = SearchProcess(problem,
                                            problem.initial, problem.goal,
                                            eval_fun, heuristic)
        self.backward_search = SearchProcess(problem,
                                             problem.goal, problem.initial,
                                             eval_fun, heuristic)

    @ property
    def search_tree(self):
        return BidirectionalSearchTreeProxy(self.forward_search.tree, self.backward_search.tree)

    def solve(self):
        upper_bound_cost = float('inf')
        while self.forward_search.can_expand_frontier() and self.backward_search.can_expand_frontier():
            upper_bound_cost = self.forward_search.expand_frontier(
                upper_bound_cost, self.backward_search)
            upper_bound_cost = self.backward_search.expand_frontier(
                upper_bound_cost, self.forward_search)

        if self.backward_search.meeting_point and self.forward_search.meeting_point:
            solution_node = self.backward_search.meeting_point.path()[0]
            meeting_point_parent = self.backward_search.meeting_point.parent
            if meeting_point_parent:
                meeting_point_parent.parent = self.forward_search.meeting_point
            else:  # meeting point is a goal node
                solution_node.parent = self.forward_search.meeting_point

            return solution_node
        return None
