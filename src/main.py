from src.problems.n_puzzle_problem import NPuzzleProblem
from src.solvers.bfs import bfs

if __name__ == '__main__':
    initialState = [[0, 1, 2], [4, 5, 3], [6, 8, 7]]
    goalState = [[0, 1, 2], [4, 5, 6], [7, 8, 9]]


    p = NPuzzleProblem(initialState, goalState)
