import pytest

from problems.blocks_world.blocks_world_problem import BlocksWorldProblem
from problems.blocks_world.blocks_world_state import BlocksWorldState
from problems.blocks_world.blocks_world_heuristic import BlocksWorldNaiveHeuristic


def assert_equal(expected, got):
    assert expected == got, f"expected to receive: {expected}, got: {got}"


# initial state is irrelevant for this case
def test_calculate_expected_columns_correctly_calculates_block_idxs():
    initial_state = None
    goal = BlocksWorldState([['A', 'B'], ['C', 'E', 'D'], []])
    heuristic = BlocksWorldNaiveHeuristic(
        BlocksWorldProblem(initial_state, goal))
    result = heuristic._calculate_expected_columns(goal)
    assert_equal({'A': 0, 'B': 0, 'C': 1, 'D': 1, 'E': 1}, result)


def test_calculate_expected_fundaments_correctly_calculates_fundaments():
    initial_state = None
    goal = BlocksWorldState([['A', 'B'], [], ['C']])
    heuristic = BlocksWorldNaiveHeuristic(
        BlocksWorldProblem(initial_state, goal))
    result = heuristic._calculate_expected_fundaments(goal)
    assert_equal({'A': [], 'B': ['A'], 'C': []}, result)


def test_returns_0_when_goal_is_reached():
    initial_state = BlocksWorldState([['A', 'B'], [], ['C']])
    goal = BlocksWorldState([['A', 'B'], [], ['C']])
    heuristic = BlocksWorldNaiveHeuristic(
        BlocksWorldProblem(initial_state, goal))
    result = heuristic(initial_state)
    assert_equal(0, result)


@pytest.mark.parametrize(
    'initial_state, goal, expected_heuristic',
    [[[('A', 'B', 'C'), (), ()], [(), ('C', 'B', 'A'), ()], 3],
     [[(), ('A', 'B', 'C'),
       ()], [('A', 'B', 'C'), (),
             ()], 3], [[('A', 'B', 'C'), (), ()], [('A', 'C', 'B'), (),
                                                   ()], 4]])
def test_heuristic(initial_state, goal, expected_heuristic):
    initial_state = BlocksWorldState(initial_state)
    goal = BlocksWorldState(goal)
    heuristic = BlocksWorldNaiveHeuristic(
        BlocksWorldProblem(initial_state, goal))
    assert_equal(heuristic(initial_state), expected_heuristic)
