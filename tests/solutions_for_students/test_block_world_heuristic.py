from problems.blocks_world.blocks_world_problem import BlocksWorldProblem
from problems.blocks_world.blocks_world_state import BlocksWorldState
from problems.blocks_world.blocks_world_heuristic import BlocksWorldNaiveHeuristic


def assert_equal(expected, got):
    assert expected == got, f"expected to receive: {expected}, got: {got}"


# initial state is irrelevant for this case
def test_calculate_expected_columns_returns_empty_dict_when_given_empty_goal_state():
    initial_state = None
    goal = BlocksWorldState([[]])
    heuristic = BlocksWorldNaiveHeuristic(
        BlocksWorldProblem(initial_state, goal))
    result = heuristic._calculate_expected_columns(goal)
    assert_equal(dict(), result)


def test_calculate_expected_columns_returns_filled_dict():
    initial_state = None
    goal = BlocksWorldState([['A'], ['B'], ['C']])
    heuristic = BlocksWorldNaiveHeuristic(
        BlocksWorldProblem(initial_state, goal))
    result = heuristic._calculate_expected_columns(goal)
    assert_equal({'A': 0, 'B': 1, 'C': 2}, result)


def test_calculate_expected_fundaments_returns_empty_dict_when_given_empty_goal_state():
    initial_state = None
    goal = BlocksWorldState([[]])
    heuristic = BlocksWorldNaiveHeuristic(
        BlocksWorldProblem(initial_state, goal))
    result = heuristic._calculate_expected_fundaments(goal)
    assert_equal(dict(), result)


def test_calculate_expected_fundaments_returns_filled_dict():
    initial_state = None
    goal = BlocksWorldState([['A', 'B'], [], ['C']])
    heuristic = BlocksWorldNaiveHeuristic(
        BlocksWorldProblem(initial_state, goal))
    result = heuristic._calculate_expected_fundaments(goal)
    assert_equal({'A': [], 'B': ['A'], 'C': []}, result)


def test_naive_heuristic_returns_0_for_all_blocks_in_correct_position():
    initial_state = BlocksWorldState([['A', 'B'], [], ['C']])
    goal = BlocksWorldState([['A', 'B'], [], ['C']])
    heuristic = BlocksWorldNaiveHeuristic(
        BlocksWorldProblem(initial_state, goal))
    result = heuristic(initial_state)
    assert_equal(0, result)


def test_naive_heuristic_returns_0_for_empty_initial_state():
    initial_state = BlocksWorldState([])
    goal = BlocksWorldState([])
    heuristic = BlocksWorldNaiveHeuristic(
        BlocksWorldProblem(initial_state, goal))
    result = heuristic(initial_state)
    assert_equal(0, result)


def test_naive_heuristic_with_correct_column_and_incorrect_blocks_order():
    initial_state = BlocksWorldState([['A', 'B', 'C'], [], []])
    goal = BlocksWorldState([['A', 'C', 'B'], [], []])
    heuristic = BlocksWorldNaiveHeuristic(
        BlocksWorldProblem(initial_state, goal))
    result = heuristic(initial_state)
    assert_equal(4, result)


def test_naive_heuristic_with_correct_order_and_incorect_column():
    initial_state = BlocksWorldState([['A', 'B', 'C'], [], []])
    goal = BlocksWorldState([[], ['A', 'B', 'C'], []])
    heuristic = BlocksWorldNaiveHeuristic(
        BlocksWorldProblem(initial_state, goal))
    result = heuristic(initial_state)
    assert_equal(3, result)


def test_naive_heuristic_with_incorrect_order_and_incorect_column():
    initial_state = BlocksWorldState([['A', 'B', 'C'], [], []])
    goal = BlocksWorldState([[], ['C', 'B', 'A'], []])
    heuristic = BlocksWorldNaiveHeuristic(
        BlocksWorldProblem(initial_state, goal))
    result = heuristic(initial_state)
    assert_equal(3, result)
