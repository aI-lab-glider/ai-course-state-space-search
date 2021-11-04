from problems.n_puzzle import NPuzzleState
from problems.n_puzzle.heuristics.n_puzzle_abstract_heuristic import NPuzzleAbstractHeuristic



class NPuzzleTilesOutOfPlaceHeuristic(NPuzzleAbstractHeuristic):

    def __call__(self, state: NPuzzleState) -> float:
        distance = 0
        state_coord = self.positions(state)
        for c, coord in state_coord.items():
            g_coord = self.goal_coords[c]
            distance += int(coord != g_coord)
        return distance