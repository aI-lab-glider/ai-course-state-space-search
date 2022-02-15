import copy

from problems.blocks_world.blocks_world_problem import BlocksWorldAction
from problems.blocks_world.blocks_world_state import BlocksWorldState


def test_world_state_does_not_change_after_applying_action():
    state = BlocksWorldState([['A', 'B', 'C'], [], []])
    state_copy = copy.deepcopy(state)
    student_action = BlocksWorldAction(0, 1)
    student_action.apply(state)
    assert state == state_copy, "action must not modify the world state"


def test_action_moves_block_to_another_column():
    state = BlocksWorldState([['A', 'B', 'C'], [], []])
    student_action = BlocksWorldAction(0, 1)
    expected_state = BlocksWorldState([['A', 'B'], ['C'], []])
    student_apply = student_action.apply(state)
    assert expected_state == student_apply, f"expected to receive: {expected_state}, got: {student_apply}"
