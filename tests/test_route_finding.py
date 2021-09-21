from problems.route_finding.location import Location
from problems.route_finding.route_finding import RouteFinding

'''
In root directory:
    $> python -m pytest 
'''
# TODO: Unittests for route finding problem.
class TestNPuzzle:
    a = Location("A", (0, 0))
    b = Location("B", (1, 1))
    c = Location("C", (2, 0))
    d = Location("D", (1, -1))
    
    pr = RouteFinding([a, b, c, d], [(a, b, 10), (b, c, 1), (a, d, 1), (d, c, 9)], a, c)

    def test_actions(self):
       pass


    def test_transition_model(self):
        pass


    def test_action_cost(self):
        pass
