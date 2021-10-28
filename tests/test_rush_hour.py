from problems.rush_hour.vehicle import RushHourVehicle, Orientation
from problems.rush_hour.board import RushHourBoard
from problems.rush_hour.rush_hour import RushHourProblem, Direction
from pytest import raises

'''
In root directory:
    $> python -m pytest 
'''

class TestRushHour:
    global x, a, b, c, d, e, f, g, o, p, q, vehicles, board, problem, d2, vehicles2, board2, problem2

    x = RushHourVehicle('X', 3, 2, Orientation.HORIZONTAL)
    a = RushHourVehicle('A', 0, 0, Orientation.HORIZONTAL)
    b = RushHourVehicle('B', 2, 0, Orientation.HORIZONTAL)
    c = RushHourVehicle('C', 4, 0, Orientation.VERTICAL)
    d = RushHourVehicle('D', 0, 1, Orientation.VERTICAL)  
    e = RushHourVehicle('E', 2, 1, Orientation.HORIZONTAL)
    f = RushHourVehicle('F', 1, 2, Orientation.VERTICAL)
    g = RushHourVehicle('G', 0, 5, Orientation.HORIZONTAL)
    o = RushHourVehicle('O', 5, 0, Orientation.VERTICAL) 
    p = RushHourVehicle('P', 2, 2, Orientation.VERTICAL)
    q = RushHourVehicle('Q', 3, 3, Orientation.HORIZONTAL)  

    vehicles = {x, a, b, c, d, e, f, g, o, p, q}
    board = RushHourBoard(vehicles) 
    problem = RushHourProblem(vehicles, board)

    d2 = RushHourVehicle('D', 0, 2, Orientation.VERTICAL) 
    vehicles2 = {x, a, b, c, d2, e, f, g, o, p, q}
    board2 = RushHourBoard(vehicles2) 
    problem2 = RushHourProblem(vehicles2, board2)
    

    def test_actions(self):
        assert set(problem.actions(board)) == set([(Direction.DOWN, 'D'), (Direction.LEFT, 'E'), (Direction.DOWN, 'F'), (Direction.UP, 'F'), (Direction.RIGHT, 'G'), (Direction.DOWN, 'P')])
        assert set(problem.actions(board)) == set([(Direction.DOWN, 'F'), (Direction.UP, 'F'), (Direction.DOWN, 'D'), (Direction.LEFT, 'E'), (Direction.RIGHT, 'G'), (Direction.DOWN, 'P')])
        assert set(problem.actions(board2)) == set([(Direction.DOWN, 'D'), (Direction.UP, 'D'), (Direction.LEFT, 'E'), (Direction.DOWN, 'F'), (Direction.UP, 'F'), (Direction.RIGHT, 'G'), (Direction.DOWN, 'P')])
        assert not set(problem.actions(board)) == set([(Direction.RIGHT, 'G'), (Direction.DOWN, 'P')])
        assert not set(problem.actions(board)) == set([(Direction.DOWN, 'F'), (Direction.UP, 'F'), (Direction.DOWN, 'D')])

    
    def test_transition_model(self):
        assert problem.transition_model(board, (Direction.DOWN, 'D')) == board2
        assert problem.transition_model(board2, (Direction.UP, 'D')) == board
        assert not problem.transition_model(board, (Direction.DOWN, 'D')) == board
        assert not problem.transition_model(board, (Direction.RIGHT, 'G')) == board2
        with raises(Exception):
            assert problem.transition_model(board, (Direction.RIGHT, 'G')) == board2


    def test_action_cost(self):
        assert problem.action_cost(board, (Direction.DOWN, 'D'), board2) == 1