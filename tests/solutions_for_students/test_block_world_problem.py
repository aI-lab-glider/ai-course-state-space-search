from problems.blocks_world.blocks_world_problem import BlocksWorldProblem
from problems.blocks_world.blocks_world_state import BlocksWorldState
from problems.blocks_world.blocks_world_action import BlocksWorldAction


def assert_equal(expected, got):
    assert expected == got, f"expected to receive: {expected}, got: {got}"


def test_actions_return_no_actions_for_empty_state():
    initial_state = BlocksWorldState([[], [], []])
    # goal is irrelevant for this case
    student_problem = BlocksWorldProblem(initial_state, goal=None)
    student_actions = student_problem.actions(initial_state)
    assert_equal([], student_actions)


def test_actions_finds_all_posible_moves():
    initial_state = BlocksWorldState([['A'], ['B'], ['C']])
    expected = [
        BlocksWorldAction(column_from=0, column_to=1),
        BlocksWorldAction(column_from=0, column_to=2),
        BlocksWorldAction(column_from=1, column_to=0),
        BlocksWorldAction(column_from=1, column_to=2),
        BlocksWorldAction(column_from=2, column_to=0),
        BlocksWorldAction(column_from=2, column_to=1)
    ]
    student_problem = BlocksWorldProblem(initial_state, None)
    assert_equal(expected, student_problem.actions(initial_state))
