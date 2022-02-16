from problems.n_puzzle.n_puzzle_state import NPuzzleState
from problems.n_puzzle.n_puzzle_problem import NPuzzleProblem
from problems.n_puzzle.heuristics.n_puzzle_manhattan_heuristic import NPuzzleManhattanHeuristic
from problems.n_puzzle.heuristics.n_puzzle_tiles_out_of_place_heuristic import NPuzzleTilesOutOfPlaceHeuristic


def assert_equal(expected, got):
    assert expected == got, f"expected to receive: {expected}, got: {got}"


def problem():
    return NPuzzleProblem(NPuzzleState([[0, 1, 2], [3, 4, 5], [
        6, 7, 8]], 0, 0), NPuzzleState([[0, 1, 2], [3, 4, 5], [6, 7, 8]], 0, 0))


def test_manhattan_heuristic_returns_0_when_puzzle_is_solved():
    heuristic = NPuzzleManhattanHeuristic(problem())
    assert_equal(0, heuristic(NPuzzleState(
        [[0, 1, 2], [3, 4, 5], [6, 7, 8]], 0, 0)))


def test_manhattan_heuristic_one_tile_misplaced():
    heuristic = NPuzzleManhattanHeuristic(problem())
    assert_equal(1, heuristic(NPuzzleState(
        [[1, 0, 2], [3, 4, 5], [6, 7, 8]], 0, 0)))


def test_manhattan_heuristic_all_tiles_misplaced():
    heuristic = NPuzzleManhattanHeuristic(problem())
    assert_equal(15, heuristic(NPuzzleState(
        [[1, 0, 3], [5, 6, 4], [2, 8, 7]], 1, 0)))


def test_n_puzzle_tiles_out_of_place_heuristic_returns_0_when_puzzle_is_solved():
    heuristic = NPuzzleTilesOutOfPlaceHeuristic(problem())
    assert_equal(0, heuristic(NPuzzleState([[0, 1, 2], [3, 4, 5], [
        6, 7, 8]], 0, 0)))


def test_n_puzzle_tiles_out_of_place_heuristic_one_tile_misplaced():
    heuristic = NPuzzleTilesOutOfPlaceHeuristic(problem())
    assert_equal(1, heuristic(NPuzzleState(
        [[1, 0, 2], [3, 4, 5], [6, 7, 8]], 0, 0)))


def test_n_puzzle_tiles_out_of_place_heuristic_all_tiles_misplaced():
    heuristic = NPuzzleTilesOutOfPlaceHeuristic(problem())
    assert_equal(8, heuristic(NPuzzleState(
        [[1, 0, 3], [5, 6, 4], [2, 8, 7]], 1, 0)))
