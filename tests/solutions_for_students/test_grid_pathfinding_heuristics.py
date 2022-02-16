from tkinter import Grid
import numpy as np
from problems.grid_pathfinding.grid_pathfinding import GridPathfinding
from problems.grid_pathfinding.grid import Grid, GridCell, GridCoord
from problems.grid_pathfinding.heuristics.diagonal_heuristic import GridDiagonalHeuristic
from problems.grid_pathfinding.heuristics.euclidean_heuristic import GridEuclideanHeuristic
from problems.grid_pathfinding.heuristics.manhattan_heuristic import GridManhattanHeuristic


def assert_equal(expected, got):
    assert expected == got, f"expected to receive: {expected}, got: {got}"


def problem():
    return GridPathfinding(
        Grid(np.full((8, 8), GridCell.EMPTY)), GridCoord(0, 0), GridCoord(0, 0), 2)


def test_diagonal_heuristic_in_a_goal_state_returns_0():
    diagonal_heuristic = GridDiagonalHeuristic(problem())
    assert_equal(0, diagonal_heuristic(GridCoord(0, 0)))


def test_diagonal_heuristic_only_diagonals():
    diagonal_heuristic = GridDiagonalHeuristic(problem())
    assert_equal(16, diagonal_heuristic(GridCoord(8, 8)))


def test_diagonal_heuristic_only_straights():
    diagonal_heuristic = GridDiagonalHeuristic(problem())
    assert_equal(8, diagonal_heuristic(GridCoord(8, 0)))


def test_diagonal_heuristic_straights_and_diagonals():
    diagonal_heuristic = GridDiagonalHeuristic(problem())
    assert_equal(12, diagonal_heuristic(GridCoord(8, 4)))


def test_euclidean_heuristic_in_a_goal_state_returns_0():
    euclidean_heuristic = GridEuclideanHeuristic(problem())
    assert_equal(0, euclidean_heuristic(GridCoord(0, 0)))


def test_euclidean_heuristic_only_straights():
    euclidean_heuristic = GridEuclideanHeuristic(problem())
    assert_equal(8, euclidean_heuristic(GridCoord(0, 8)))


def test_euclidean_heuristic_straights_and_diagonals():
    euclidean_heuristic = GridEuclideanHeuristic(problem())
    assert_equal(5, euclidean_heuristic(GridCoord(3, 4)))


def test_manhattan_heuristic_in_a_goal_state_returns_0():
    manhattan_heuristic = GridManhattanHeuristic(problem())
    assert_equal(0, manhattan_heuristic(GridCoord(0, 0)))


def test_manhattan_heuristic_only_straights():
    manhattan_heuristic = GridManhattanHeuristic(problem())
    assert_equal(5, manhattan_heuristic(GridCoord(5, 0)))


def test_manhattan_heuristic_with_diagonals():
    manhattan_heuristic = GridManhattanHeuristic(problem())
    assert_equal(13, manhattan_heuristic(GridCoord(5, 8)))
