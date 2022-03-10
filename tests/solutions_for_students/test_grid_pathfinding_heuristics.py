from tkinter import Grid
import numpy as np
import pytest

from problems.grid_pathfinding.grid_pathfinding import GridPathfinding
from problems.grid_pathfinding.grid import Grid, GridCell, GridCoord
from problems.grid_pathfinding.heuristics.diagonal_heuristic import GridDiagonalHeuristic
from problems.grid_pathfinding.heuristics.euclidean_heuristic import GridEuclideanHeuristic
from problems.grid_pathfinding.heuristics.manhattan_heuristic import GridManhattanHeuristic


def assert_equal(expected, got):
    assert expected == got, f"expected to receive: {expected}, got: {got}"


@pytest.fixture
def problem():
    return GridPathfinding(Grid(np.full((8, 8), GridCell.EMPTY)),
                           GridCoord(0, 0), GridCoord(0, 0), 2)


@pytest.mark.parametrize('expected_heuristic_value, target_coord',
                         [[0, GridCoord(0, 0)], [16, GridCoord(8, 8)],
                          [8, GridCoord(8, 0)], [12, GridCoord(8, 4)]])
def test_diagonal_heuristic(problem, expected_heuristic_value, target_coord):
    print(expected_heuristic_value, target_coord)
    diagonal_heuristic = GridDiagonalHeuristic(problem)
    assert_equal(expected_heuristic_value, diagonal_heuristic(target_coord))


@pytest.mark.parametrize(
    'expected_heuristic_value, target_coord',
    [[0, GridCoord(0, 0)], [8, GridCoord(0, 8)], [5, GridCoord(3, 4)]])
def test_euclidean_heuristic(problem, expected_heuristic_value, target_coord):
    print(expected_heuristic_value, target_coord)
    diagonal_heuristic = GridEuclideanHeuristic(problem)
    assert_equal(expected_heuristic_value, diagonal_heuristic(target_coord))


@pytest.mark.parametrize(
    'expected_heuristic_value, target_coord',
    [[0, GridCoord(0, 0)], [5, GridCoord(5, 0)], [13, GridCoord(5, 8)]])
def test_manhattan_heuristic(problem, expected_heuristic_value, target_coord):
    print(expected_heuristic_value, target_coord)
    diagonal_heuristic = GridManhattanHeuristic(problem)
    assert_equal(expected_heuristic_value, diagonal_heuristic(target_coord))
