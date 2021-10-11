from problems.rush_hour.vehicle import RushHourVehicle
from problems.rush_hour.board import RushHourBoard
from problems.rush_hour.rush_hour import RushHourProblem
from pytest import raises

'''
In root directory:
    $> python -m pytest 
'''

class TestRushHour:
    global x, a, b, c, d, e, f, g, o, p, q, vehicles, board, problem, d2, vehicles2, board2, problem2

    x = RushHourVehicle('X', 3, 2, 'H')
    a = RushHourVehicle('A', 0, 0, 'H')
    b = RushHourVehicle('B', 2, 0, 'H')
    c = RushHourVehicle('C', 4, 0, 'V')
    d = RushHourVehicle('D', 0, 1, 'V')  
    e = RushHourVehicle('E', 2, 1, 'H')
    f = RushHourVehicle('F', 1, 2, 'V')
    g = RushHourVehicle('G', 0, 5, 'H')
    o = RushHourVehicle('O', 5, 0, 'V') 
    p = RushHourVehicle('P', 2, 2, 'V')
    q = RushHourVehicle('Q', 3, 3, 'H') 

    vehicles = {x, a, b, c, d, e, f, g, o, p, q}
    board = RushHourBoard(vehicles) 
    problem = RushHourProblem(vehicles, board)

    d2 = RushHourVehicle('D', 0, 2, 'V') 
    vehicles2 = {x, a, b, c, d2, e, f, g, o, p, q}
    board2 = RushHourBoard(vehicles2) 
    problem2 = RushHourProblem(vehicles2, board2)
    

    def test_actions(self):
        assert set(problem.actions(board)) == set([('down', 'D'), ('left', 'E'), ('down', 'F'), ('up', 'F'), ('right', 'G'), ('down', 'P')])
        assert set(problem.actions(board)) == set([('down', 'F'), ('up', 'F'), ('down', 'D'), ('left', 'E'), ('right', 'G'), ('down', 'P')])
        assert set(problem.actions(board2)) == set([('down', 'D'), ('up', 'D'), ('left', 'E'), ('down', 'F'), ('up', 'F'), ('right', 'G'), ('down', 'P')])
        assert not set(problem.actions(board)) == set([('right', 'G'), ('down', 'P')])
        assert not set(problem.actions(board)) == set([('down', 'F'), ('up', 'F'), ('down', 'D')])

    
    def test_transition_model(self):
        assert problem.transition_model(board, ('down', 'D')) == board2
        assert problem.transition_model(board2, ('up', 'D')) == board
        assert not problem.transition_model(board, ('down', 'D')) == board
        assert not problem.transition_model(board, ('right', 'G')) == board2
        with raises(Exception):
            assert problem.transition_model(board, ('right', 'G')) == board2


    def test_action_cost(self):
        assert problem.action_cost(board, ('down', 'D'), board2) == 1