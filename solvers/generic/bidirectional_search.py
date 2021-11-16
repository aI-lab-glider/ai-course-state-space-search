from __future__ import annotations
import traceback
from typing import Any, Callable, Optional
from PIL.Image import new

from numpy import ubyte
from base.heuristic import Heuristic, NoHeuristic
from base.problem import ReversibleProblem, Problem
from base.state import State
from solvers.utils import PriorityQueue
from tree.node import Node
from tree.tree import NodeEventSubscriber, Tree


class SearchProcess:
    def __init__(self, 
                 problem: Problem,
                 start_state: State,
                 heuristic: Heuristic = NoHeuristic()):
        self.problem = problem
        self.heuristic = heuristic
        self.tree = Tree(Node(start_state))
        self.frontier = self._new_priority_queue(self.tree.root)
        self.meeting_point = self.tree.root
        self.cost_lower_bound = float('inf')
        self.rejected_states = set()
        self.visited_states = {self.tree.root.state: self.tree.root}

    def state_node(self, state: State) -> Node | None:
        return self.visited_states.get(state, None)

    def state_cost(self, state: State):
        if state in self.visited_states:
            return self.visited_states[state].cost
        return float('inf')

    def has_visited_state(self, state: State):
        return state in self.visited_states

    def can_expand_frontier(self):
        return not self.frontier.is_empty()
    
    def expand_frontier(self, upper_bound: float, opposite: SearchProcess) -> float:
        """
        Makes actual search logic by expanding valid nodes and labeling (assigning cost values) them.

        Args: 
            upper_bound_cost: cost of best path found until now. Equals to inf, if process, hasn't met before
            opposite: instance that searches tree from the opposite node
        """
        candidates = self._find_candidates(upper_bound)
        candidate = self._select_candidate(candidates, upper_bound, opposite)
        if candidate is not None:
            self.cost_lower_bound = self.state_cost(candidate.state) + self.heuristic(candidate.state)
            if not opposite.has_visited_state(candidate.state):
                for node in self.tree.expand(self.problem, candidate):
                    if node.state in self.rejected_states:
                        continue
                    if not self.has_visited_state(node.state) or self.state_cost(node.state) > node.cost:
                        self.visited_states[node.state] = node
                        self.frontier.push(node)
                        upper_bound = self._calculate_upper_bound(node, upper_bound, opposite)
        return upper_bound

    def _new_priority_queue(self, *nodes: Node) -> PriorityQueue:
        return PriorityQueue(self._estimated_cost, list(nodes))

    def _estimated_cost(self, n: Node) -> float:
        return n.cost + self.heuristic(n.state)

    def _find_candidates(self, upper_bound_cost: float) -> PriorityQueue:
        """
        Returns priority queue containing only nodes with smaller estimate value,
        than actual upper bound cost.
        """
        candidates = self._new_priority_queue()
        while not self.frontier.is_empty():
            candidate = self.frontier.pop()
            if self._estimated_cost(candidate) < upper_bound_cost:
                candidates.push(candidate)
        return candidates

    def _select_candidate(self, 
                          candidates: PriorityQueue[Node], 
                          upper_bound: float,
                          opposite: 'SearchProcess') -> Optional[Node]:
        """
        Returns a node, that wasn't visited by another process, or was visited but 
        that path resulted in a higher cost. 
        """
        chosen = None
        while candidates and not chosen:
            candidate = candidates.pop()
            cost_through_state = self.state_cost(candidate.state) + opposite.cost_lower_bound + opposite.heuristic(candidate.state)
            if not opposite.has_visited_state(candidate.state) and upper_bound < float('inf') and cost_through_state >= upper_bound:
                self.rejected_states.add(candidate.state)
            else:
                chosen = candidate
        return chosen

    def _calculate_upper_bound(self, node: Node, upper_bound_cost: float, other_process: 'SearchProcess') -> float:
        """
        Calculates new upper bound and sets meeting point to node in case, if it promises shorter path.
        """
        new_upper_bound_cost = self.state_cost(node.state) + other_process.state_cost(node.state)
        if new_upper_bound_cost < upper_bound_cost:
            upper_bound_cost = new_upper_bound_cost
            self.meeting_point = node
        return upper_bound_cost


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


class BidirectionalSearch:

    def __init__(self, problem: ReversibleProblem[State, Any], 
                       primary_heuristic: Heuristic[State],
                       opposite_heuristic: Heuristic[State]):
        self.problem = problem
        self.primary_search = SearchProcess(problem,
                                            problem.initial,
                                            primary_heuristic)
        self.opposite_search = SearchProcess(problem,
                                             problem.goal,
                                             opposite_heuristic)

    @property
    def search_tree(self):
        return BidirectionalSearchTreeProxy(self.primary_search.tree, self.opposite_search.tree)

    def solve(self):
        upper_bound_cost = float('inf')
        while self.primary_search.can_expand_frontier() and self.opposite_search.can_expand_frontier():
            upper_bound_cost = self.primary_search.expand_frontier(
                upper_bound_cost, self.opposite_search)
            upper_bound_cost = self.opposite_search.expand_frontier(
                upper_bound_cost, self.primary_search)  
    
        if self.opposite_search.meeting_point and self.primary_search.meeting_point:
            return self._join_paths(self.primary_search.meeting_point, self.opposite_search.meeting_point)
        return None
    
    def _join_paths(self, primary: Node, opposite: Node):
        if opposite.state in self.primary_search.visited_states: 
            primary = self.primary_search.visited_states[opposite.state]    
        elif primary.state in self.opposite_search.visited_states:
            opposite = self.opposite_search.visited_states[primary.state]
        
        current_node = opposite.reverse(primary.cost)
        join_point = current_node.root()
        join_point.parent = primary.parent
        return current_node