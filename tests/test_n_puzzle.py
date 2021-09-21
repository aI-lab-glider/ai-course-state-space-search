from problems.n_puzzle.n_puzzle_problem import NPuzzleProblem
from problems.n_puzzle.n_puzzle_state import NPuzzleState

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

        assert set(p.actions(state)) == set(["up", "down", "right"])
        assert set(p.actions(state)) == set(["down", "up", "right"])
        assert set(p.actions(state)) == set(["right", "down", "up"])

    def test_actions_false(self):
        matrix =[[3, 1, 2],
                [6, 4, 5],
                [0, 7, 8]]

        state = NPuzzleState(matrix, 2, 0)
        p = NPuzzleProblem(state)

        assert not set(p.actions(state)) == set(["right"])
        assert not set(p.actions(state)) == set(["up"])
        assert not set(p.actions(state)) == set(["up", "right", "down"])


    def test_transition_model(self):
        matrix = [[3, 1, 2],
                  [0, 4, 5],
                  [6, 7, 8]]
                  
        state = NPuzzleState(matrix, 1, 0)
        p = NPuzzleProblem(state)

        matrix2 = [[0, 1, 2],
                  [3, 4, 5],
                  [6, 7, 8]]
        state2 = NPuzzleState(matrix2, 0, 0)

        assert p.transition_model(state, "up") == state2
        assert not p.transition_model(state, "down") == state2


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

        assert p.action_cost(state, "up", state2) == 1
