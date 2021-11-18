from __future__ import annotations
from typing import Any, Optional, Set

from base.heuristic import Heuristic, NoHeuristic
from base.problem import ReversibleProblem, Problem
from base.state import State
from solvers.utils import PriorityQueue
from tree.node import Node
from tree.tree import NodeEventSubscriber, Tree



class SearchProcess():
    """
    A single search process in the bidirectional approach.

    Attributes:
    ===========
    problem: Problem
        solved problem, passed in the constructor
    start_state: State
        state where the process starts the search
        passed in the constructor
    heuristic: Heuristic
        heuristic used to guide the search
        passed in the constructor
    tree: Tree
        search tree associated with the search
        set up in the __init__
    frontier: PriorityQueue
        a queue with nodes left to be explored
        set up in the __init__
    meeting_point: Optional[Node]
        current best node shared with the opposing search process
        set up in the __init__
    cost_lower_bound: float
        the current lower bound on the solutions
    rejected_states: Set[State]
        set containing all the nodes that don't have to be explored
    scanned_states: Set[State]
        set containing all the nodes that have been expanded
    labeled_states: Dict[State, Node]
        this dictionary contains all the nodes that wait to be expanded
        one access the node by the corresponding state

    Methods:
    ========
    labeled_node(state: State) -> Optional[Node]
        returns labeled node assiociated with the given state
        returns None, if there is no such node
    labeled_state_cost(state: State) -> float
        if the state is labeled, return an associated cost
        otherwise returns +inf
    has_labeled_state(state: State) -> bool
        returns whether the state has been labeled
    has_scanned_state(state: State) -> bool:
        returns whether the state has been scanned
    expand_frontier(upper_bound: float, opposite: SearchProcess) -> Optional[float]
        performs a single step of the search process, i.e. expands single viable node from the frontier
        uses current upper bound and info from opposite search to prune the search tree
        returns None if there are no more nodes to be expanded
        otherwise returns updated upper bound
    """
    def __init__(self, 
                 problem: Problem,
                 start_state: State,
                 heuristic: Heuristic = NoHeuristic()):
        self.problem = problem
        self.heuristic = heuristic
        self.tree = Tree(Node(start_state))
        self.frontier = PriorityQueue(self._estimated_cost, [self.tree.root])
        self.meeting_point : Optional[Node] = None
        self.cost_lower_bound = float('inf')
        self.rejected_states : Set[State] = set()
        self.scanned_states : Set[State] = set()
        self.labeled_states = {self.tree.root.state: self.tree.root}

    def labeled_node(self, state: State) -> Optional[Node]:
        return self.labeled_states.get(state, None)

    def labeled_state_cost(self, state: State) -> float:
        if self.has_labeled_state(state):
            return self.labeled_states[state].cost
        return float('inf')

    def has_labeled_state(self, state: State) -> bool:
        return state in self.labeled_states

    def has_scanned_state(self, state: State) -> bool:
        return state in self.scanned_states
    
    def expand_frontier(self, upper_bound: float, opposite: SearchProcess) -> Optional[float]:
        # TODO:
        # 1. find a new node to expand
        #   - if there is no such node, return None, this marks end of the process
        # 2. Mark the node as scanned (add it to the self.scanned_states)
        # 3. Update the lower bound if the estimated value for the state is lower than the current one
        # 4. if the opposite process hasn't scanned the node's state yet:
        #   - iterate over all the children of the node, that haven't been rejected/scanned
        #   - if their states have been labeled already, check if they have a better cost (like in the normal A*)
        #   - if those conditions hold:
        #       * label the new node and add it to the frontier
        #       * update the upper bound
        # 5. return the current upper bound 
        candidate = self._select_candidate(upper_bound, opposite)
        if candidate is None:
            return None

        self.scanned_states.add(candidate.state)
        self.cost_lower_bound = min(self.cost_lower_bound, \
                        self.labeled_state_cost(candidate.state) + self.heuristic(candidate.state))

        if not opposite.has_scanned_state(candidate.state):
            for node in self.tree.expand(self.problem, candidate):
                if node.state in self.rejected_states or node.state in self.scanned_states:
                    continue
                if not self.has_labeled_state(node.state) or self.labeled_state_cost(node.state) > node.cost:
                    self.labeled_states[node.state] = node
                    self.frontier.push(node)
                    upper_bound = self._update_upper_bound(node, upper_bound, opposite)
                    
        return upper_bound

    def _estimated_cost(self, n: Node) -> float:
        """ returns estimated cost of the given node"""
        return n.cost + self.heuristic(n.state)

    def _select_candidate(self, 
                          upper_bound: float,
                          opposite: 'SearchProcess') -> Optional[Node]:
        # TODO:
        # - return the first node from the frontier that:
        #   * has estimated cost lower than the upper bound
        #   * has bidirectional estimate lower than the lower bound
        # - if there is no such node, return None   
        # - all the nodes that failed those tests should end up in the self.rejected_states (their states, to be exact)
        # tip. bidirectional estimate = labeled cost + lower bound of the opposite process - opposite heuristic 
        chosen = None
        while self.frontier and not chosen:
            candidate = self.frontier.pop()
            if self._estimated_cost(candidate) >= upper_bound:
                self.rejected_states.add(candidate.state)
                continue

            cost_through_state = self.labeled_state_cost(candidate.state) + opposite.cost_lower_bound - opposite.heuristic(candidate.state)
            if not opposite.has_scanned_state(candidate.state) and upper_bound < float('inf') and cost_through_state >= upper_bound:
                self.rejected_states.add(candidate.state)
                continue
            
            chosen = candidate
        return chosen

    def _update_upper_bound(self, node: Node, upper_bound_cost: float, other_process: 'SearchProcess') -> float:
        # TODO:
        # 1. calculate new upper bound based on the node
        # 2. if the new upper bound is better than the old one:
        #    - update the self.meeting_point to the node
        #    - return the new upper bound
        # 3. otherwise return the old one
        # tip. upper bound of the path given a node is the sum of of the node's labeled cost in both processes
        new_upper_bound_cost = self.labeled_state_cost(node.state) + other_process.labeled_state_cost(node.state)
        if new_upper_bound_cost < upper_bound_cost:
            upper_bound_cost = new_upper_bound_cost
            self.meeting_point = node
        return upper_bound_cost


class BidirectionalSearchTreeProxy(Tree, NodeEventSubscriber):
    """
    Wrapper over the search tree to handle bidirectional search
    """
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
        """
        Runs both search processes until the end of the search.
        """
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
    
        if self.opposite_search.meeting_point or self.primary_search.meeting_point:
            return self._join_paths(self.primary_search.meeting_point, self.opposite_search.meeting_point)
        return None
    
    def _join_paths(self, primary: Node, opposite: Node):
        """
        Merges primary and opposite paths into a single solution path
        """
        if opposite is not None and self.primary_search.has_labeled_state(opposite.state): 
            node = self.primary_search.labeled_node(opposite.state) 
            assert node is not None
            primary = node            
        elif primary and primary.state in self.opposite_search.labeled_states:
            node = self.opposite_search.labeled_node(primary.state) 
            assert node is not None
            opposite = node
        
        current_node = opposite.reverse(primary.cost)
        join_point = current_node.root()
        join_point.parent = primary.parent
        return current_node