from pytest import raises
from numpy import inf
from problems.route_finding.location import Location
from problems.route_finding.route_finding import RouteFinding

'''
In root directory:
    $> python3 -m pytest 
'''

class TestRouteFinding:
    global pr, a, b, c, d
    a = Location("A", (0, 0))
    b = Location("B", (1, 1))
    c = Location("C", (2, 0))
    d = Location("D", (1, -1))
    
    pr = RouteFinding([a, b, c, d], [(a, b, 0), (b, c, 1), (a, d, 1), (d, c, 9)], a, c)

    def test_actions(self):
        actions = []
        for action in pr.actions(a):
            actions.append(action)

        assert set(actions) == set(["D", "B"])
        assert not  set(actions) == set(["B"])
        assert not  set(actions) == set(["D"])


    def test_transition_model(self):
        assert pr.transition_model(a, "B") == "B"
        assert not pr.transition_model(a, "B") == "A"
        with raises(AssertionError):
            assert (pr.transition_model(a, "C") == "D")


    def test_action_cost(self):
        assert pr.action_cost(a, "B", b) == 0
        assert pr.action_cost(b, "C", c) == 1
        assert not pr.action_cost(a, "B", b) == inf
