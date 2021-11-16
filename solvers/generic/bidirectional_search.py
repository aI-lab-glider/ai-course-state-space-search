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
        self.frontier = PriorityQueue(self._estimated_cost, [self.tree.root])
        self.meeting_point = self.tree.root
        self.cost_lower_bound = float('inf')
        self.rejected_states = set()
        self.scanned_states = set()
        self.visited_states = {self.tree.root.state: self.tree.root}

    def state_node(self, state: State) -> Node | None:
        return self.visited_states.get(state, None)

    def state_cost(self, state: State):
        if state in self.visited_states:
            return self.visited_states[state].cost
        return float('inf')

    def has_visited_state(self, state: State):
        return state in self.visited_states

    def has_scanned_state(self, state: State):
        return state in self.scanned_states
    
    def expand_frontier(self, upper_bound: float, opposite: SearchProcess) -> float | None:
        """
        Makes actual search logic by expanding valid nodes and labeling (assigning cost values) them.

        Args: 
            upper_bound: cost of best path found until now. Equals to inf, if process, hasn't met before
            opposite: instance that searches tree from the opposite node
        """
        candidate = self._select_candidate(upper_bound, opposite)
        if candidate is None:
            return None

        self.scanned_states.add(candidate)
        self.cost_lower_bound = min(self.cost_lower_bound, \
                        self.state_cost(candidate.state) + self.heuristic(candidate.state))

        if not opposite.has_scanned_state(candidate.state):
            for node in self.tree.expand(self.problem, candidate):
                if node.state in self.rejected_states or node.state in self.scanned_states:
                    continue
                if not self.has_visited_state(node.state) or self.state_cost(node.state) > node.cost:
                    self.visited_states[node.state] = node
                    self.frontier.push(node)
                    upper_bound = self._calculate_upper_bound(node, upper_bound, opposite)
                    
        return upper_bound

    def _estimated_cost(self, n: Node) -> float:
        return n.cost + self.heuristic(n.state)

    def _select_candidate(self, 
                          upper_bound: float,
                          opposite: 'SearchProcess') -> Optional[Node]:
        """
        Returns a node, that wasn't visited by another process, or was visited but 
        that path resulted in a higher cost. 
        """
        chosen = None
        while self.frontier and not chosen:
            candidate = self.frontier.pop()
            if self._estimated_cost(candidate) >= upper_bound:
                self.rejected_states.add(candidate.state)
                continue

            cost_through_state = self.state_cost(candidate.state) + opposite.cost_lower_bound - opposite.heuristic(candidate.state)
            if not opposite.has_scanned_state(candidate.state) and upper_bound < float('inf') and cost_through_state >= upper_bound:
                self.rejected_states.add(candidate.state)
                continue
            
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
        while True:
            upper_bound_cost = self.primary_search.expand_frontier(
                upper_bound_cost, self.opposite_search)
            if upper_bound_cost is None:
                break 

            upper_bound_cost = self.opposite_search.expand_frontier(
                upper_bound_cost, self.primary_search)  
            if upper_bound_cost is None:
                break
    
        if self.opposite_search.meeting_point and self.primary_search.meeting_point:
            return self._join_paths(self.primary_search.meeting_point, self.opposite_search.meeting_point)
        return None
    
    def _join_paths(self, primary: Node, opposite: Node):
        if self.primary_search.has_visited_state(opposite.state): 
            primary = self.primary_search.state_node(opposite.state) 
        elif primary.state in self.opposite_search.visited_states:
            opposite = self.opposite_search.state_node(primary.state)
        
        current_node = opposite.reverse(primary.cost)
        join_point = current_node.root()
        join_point.parent = primary.parent
        return current_node