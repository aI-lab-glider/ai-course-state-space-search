import pytest

from problems.n_puzzle.n_puzzle_state import NPuzzleState
from problems.n_puzzle.n_puzzle_problem import NPuzzleProblem
from problems.n_puzzle.heuristics.n_puzzle_manhattan_heuristic import NPuzzleManhattanHeuristic
from problems.n_puzzle.heuristics.n_puzzle_tiles_out_of_place_heuristic import NPuzzleTilesOutOfPlaceHeuristic


def assert_equal(expected, got):
    assert expected == got, f"expected to receive: {expected}, got: {got}"


@pytest.fixture
def problem():
    return NPuzzleProblem(
        NPuzzleState([[0, 1, 2], [3, 4, 5], [6, 7, 8]], 0, 0),
        NPuzzleState([[0, 1, 2], [3, 4, 5], [6, 7, 8]], 0, 0))


@pytest.mark.parametrize(
    'expected_heuristic_value, current_state',
    [[0, NPuzzleState([[0, 1, 2], [3, 4, 5], [6, 7, 8]], 0, 0)],
     [1, NPuzzleState([[1, 0, 2], [3, 4, 5], [6, 7, 8]], 0, 0)],
     [15, NPuzzleState([[1, 0, 3], [5, 6, 4], [2, 8, 7]], 1, 0)]])
def test_manhattan_heuristic(problem, expected_heuristic_value, current_state):
    heuristic = NPuzzleManhattanHeuristic(problem)
    assert_equal(expected_heuristic_value, heuristic(current_state))


@pytest.mark.parametrize(
    'expected_heuristic_value, current_state',
    [[0, NPuzzleState([[0, 1, 2], [3, 4, 5], [6, 7, 8]], 0, 0)],
     [1, NPuzzleState([[1, 0, 2], [3, 4, 5], [6, 7, 8]], 0, 0)],
     [8, NPuzzleState([[1, 0, 3], [5, 6, 4], [2, 8, 7]], 1, 0)]])
def test_n_puzzle_tiles_out_of_place_heuristic(problem,
                                               expected_heuristic_value,
                                               current_state):
    heuristic = NPuzzleTilesOutOfPlaceHeuristic(problem)
    assert_equal(expected_heuristic_value, heuristic(current_state))
