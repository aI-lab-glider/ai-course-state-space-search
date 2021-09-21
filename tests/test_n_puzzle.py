from src.problems.n_puzzle.n_puzzle_problem import NPuzzleProblem
from src.problems.n_puzzle.n_puzzle_state import NPuzzleState

'''
In root directory:
    $> python -m pytest 
'''

class TestNPuzzle:
    def test_actions(self):
        matrix = [[3, 1, 2],
                  [0, 4, 5],
                  [6, 7, 8]]

        state = NPuzzleState(matrix, 1, 0)
        p = NPuzzleProblem(state)

        assert p.actions(state) == ["down", "up", "right"]


    def test_transition_model(self):
        matrix = [[3, 1, 2],
                  [0, 4, 5],
                  [6, 7, 8]]
        state = NPuzzleState(matrix, 1, 0)
        p = NPuzzleProblem(NPuzzleState(matrix, 1, 0)) 

        matrix2 = [[0, 1, 2],
                  [3, 4, 5],
                  [6, 7, 8]]
        state2 = NPuzzleState(matrix2, 0, 0)
        assert p.transition_model(state,"up") == state2


    def test_action_cost(self):
        matrix = [[3, 1, 2],
                  [0, 4, 5],
                  [6, 7, 8]]
        state = NPuzzleState(matrix, 1, 0)
        p = NPuzzleProblem(NPuzzleState(matrix, 1, 0)) 

        matrix2 = [[0, 1, 2],
                  [3, 4, 5],
                  [6, 7, 8]]
        state2 = NPuzzleState(matrix2, 0, 0)
        assert p.action_cost(state,"up",state2) == 1
