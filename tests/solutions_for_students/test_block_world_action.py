import copy

from problems.blocks_world.blocks_world_problem import BlocksWorldAction
from problems.blocks_world.blocks_world_state import BlocksWorldState


def test_action_does_not_mutate_parent_state():
    state = BlocksWorldState([['A', 'B', 'C'], [], []])
    state_copy = copy.deepcopy(state)
    action = BlocksWorldAction(0, 1)
    action.apply(state)
    assert state == state_copy, "action must not modify the world state"


def test_action_moves_block_to_another_column():
    state = BlocksWorldState([['A', 'B', 'C'], [], []])
    action = BlocksWorldAction(0, 1)
    expected_state = BlocksWorldState([['A', 'B'], ['C'], []])
    student_apply = action.apply(state)
    assert expected_state == student_apply, f"expected to receive: {expected_state}, got: {student_apply}"
