from queue import Queue as FifoQueue
from base.problem import Problem
from tree import Node, Tree
from base import Solver


class BFS(Solver):
    def __init__(self, problem:Problem):
        super().__init__(problem)

    def run():
        

def BFS(problem, state):
    node = Node(state)
    tree = Tree(node)
    if problem.is_goal(node.state):
        return node
    frontier = FifoQueue()
    visited = {state}
    while not frontier.empty():
        node = frontier.get()
        for child_node in tree.expand(problem, node):
            if problem.is_goal(child_node.state):
                return child_node
            if child_node.state not in visited:
                frontier.put(child_node.state)
                visited.add(child_node.state)
    return None



