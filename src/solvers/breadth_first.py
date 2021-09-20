from queue import Queue as FifoQueue
from tree import Node, Tree


class BFS:
    def __init__(self, problem, state):
        self.problem = problem
        self.start = state
        self.frontier = FifoQueue()
        self.visited = {self.start}
        self.root= Node(self.start)
        self.tree = Tree(self.root)


    def run(self):
        if self.problem.is_goal(self.root.state):
            return self.root
        self.frontier.put(self.root)
        while self.frontier:
            parent = self.frontier.get()
            for child_node in self.tree.expand(self.problem, parent):
                if self.problem.is_goal(child_node.state):
                    return child_node
                if child_node.state not in self.visited:
                    self.frontier.put(child_node)
                    self.visited.add(child_node.state)
        return None


