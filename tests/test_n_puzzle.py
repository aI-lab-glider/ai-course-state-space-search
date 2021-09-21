from problems.n_puzzle.n_puzzle_problem import NPuzzleProblem
from problems.n_puzzle.n_puzzle_state import NPuzzleState
from pytest import raises

'''
In root directory:
    $> python -m pytest 
'''

class TestNPuzzle:
    global matrix, matrix2, state, state2, p
    matrix =    [[3, 1, 2],
                [0, 4, 5],
                [6, 7, 8]]
    matrix2 =   [[0, 1, 2],
                [3, 4, 5],
                [6, 7, 8]]

    state = NPuzzleState(matrix, 1, 0)
    state2 = NPuzzleState(matrix2, 0, 0)
    p = NPuzzleProblem(state)


    def test_actions(self):
        assert set(p.actions(state)) == set(["up", "down", "right"])
        assert set(p.actions(state)) == set(["down", "up", "right"])
        assert set(p.actions(state)) == set(["right", "down", "up"])
        assert not set(p.actions(state)) == set(["right"])
        assert not set(p.actions(state)) == set(["up"])
        assert not set(p.actions(state)) == set(["up", "right", "down", "left"])


    def test_transition_model(self):
        assert p.transition_model(state, "up") == state2
        assert not p.transition_model(state, "down") == state2
        with raises(Exception):
            assert p.transition_model(state, "down") == state2


    def test_action_cost(self):
        assert p.action_cost(state, "up", state2) == 1
