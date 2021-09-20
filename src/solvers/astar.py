from solvers.best_first import BestFirstSearch


class AStar(BestFirstSearch):
    def __init__(self, problem, state, heuristic):
        super().__init__(problem, state, eval_fun=lambda node: node.cost + heuristic(node.state))
        
        