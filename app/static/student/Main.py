import sys, os
sys.path.append(os.path.abspath('../../../'))
import Board as brd

Board = brd.Board(10, 40)


def drawBoard():
    Board.place_start(2, 3)
    Board.place_finish(5, 20)
    Board.place_wall(8, 4)
    Board.place_wall(8, 3)
    for i in range(0, 9):
        Board.place_wall(i, 16)
    for i in range(17, 25):
        Board.place_wall(8, i)
    return Board.data

def solveBFS():
    Board.BFS()
    Board.print_path(Board.matrix[Board.x_finish][Board.y_finish])
    return Board.data
