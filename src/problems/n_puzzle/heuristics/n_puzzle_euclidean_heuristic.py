from problems.n_puzzle import NPuzzleState
from math import sqrt

from problems.n_puzzle.heuristics.n_puzzle_abstract_heuristic import NPuzzleAbstractHeuristic



class NPuzzleEuclideanHeuristic(NPuzzleAbstractHeuristic):

    def __call__(self, state: NPuzzleState) -> float:
        distance = 0
        state_coord = self.positions(state)
        for c, coord in state_coord.items():
            g_coord = self.goal_coords[c]
            distance += sqrt((coord[0] - g_coord[0])**2 + (coord[1] - g_coord[1])**2)
        return distance