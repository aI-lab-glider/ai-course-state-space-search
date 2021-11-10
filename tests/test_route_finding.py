# from pytest import raises
# from numpy import inf
# from problems.grid_pathfinding.location import Location
# from problems.grid_pathfinding.grid_pathfinding import RouteFinding

# '''
# In root directory:
#     $> python -m pytest 
# '''

# class TestRouteFinding:
#     global pr, a, b, c, d
#     a = Location("A", (0, 0))
#     b = Location("B", (1, 1))
#     c = Location("C", (2, 0))
#     d = Location("D", (1, -1))
    
#     pr = RouteFinding([a, b, c, d], [(a, b, 0), (b, c, 1), (a, d, 1), (d, c, 9)], a, c)

#     def test_actions(self):
#         actions = []
#         for action in pr.actions(a):
#             actions.append(action)

#         assert set(actions) == set(["D", "B"])
#         assert not  set(actions) == set(["B"])
#         assert not  set(actions) == set(["D"])


#     def test_take_action(self):
#         assert pr.take_action(a, "B") == "B"
#         assert not pr.take_action(a, "B") == "A"
#         with raises(AssertionError):
#             assert (pr.take_action(a, "C") == "D")


#     def test_action_cost(self):
#         assert pr.action_cost(a, "B", b) == 0
#         assert pr.action_cost(b, "C", c) == 1
#         assert not pr.action_cost(a, "B", b) == inf
