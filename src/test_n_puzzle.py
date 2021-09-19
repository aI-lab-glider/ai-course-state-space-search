import unittest
from problems.n_puzzle import NPuzzleProblem
from problems.n_puzzle import NPuzzleState



"""
python -m unittest test_n_puzzle.py

z dobrą definicją main: python test_n_puzzle.py

wszystkie testy zaczynają się słowem test

"""

class TestNPuzzle(unittest.TestCase):
    
    def test_actions(self):
        matrix = [[3, 1, 2],
                  [0, 4, 5],
                  [6, 7, 8]]
        state = NPuzzleState(matrix, 1, 0)
        p = NPuzzleProblem(NPuzzleState(matrix, 1, 0)) 
        self.assertEqual(p.actions(state),["down", "up", "right"])


        matrix = [[3, 1, 2],
                  [4, 0, 5],
                  [6, 7, 8]]
        state = NPuzzleState(matrix, 1, 1)
        self.assertEqual(p.actions(state),["down", "up", "right", "left"])

        matrix = [[3, 1, 0],
                  [4, 2, 5],
                  [6, 7, 8]]
        state = NPuzzleState(matrix, 0, 2)
        self.assertEqual(p.actions(state),["down", "left"])

        matrix = [[3, 1, 2],
                  [4, 8, 5],
                  [6, 7, 0]]
        state = NPuzzleState(matrix, 2, 2)
        self.assertEqual(p.actions(state),["up","left"])
        


    def test_transition_model(self):

        matrix = [[3, 1, 2],
                  [0, 4, 5],
                  [6, 7, 8]]
        state = NPuzzleState(matrix, 1, 0)
        p = NPuzzleProblem(NPuzzleState(matrix, 1, 0)) 

        matrix2 = [[0, 1, 2],
                  [3, 4, 5],
                  [6, 7, 8]]
        state2 = NPuzzleState(matrix2, 0, 0)
        self.assertEqual(p.transition_model(state,"up"),state2)

    def test_action_cost(self):
        matrix = [[3, 1, 2],
                  [0, 4, 5],
                  [6, 7, 8]]
        state = NPuzzleState(matrix, 1, 0)
        p = NPuzzleProblem(NPuzzleState(matrix, 1, 0)) 

        matrix2 = [[0, 1, 2],
                  [3, 4, 5],
                  [6, 7, 8]]
        state2 = NPuzzleState(matrix2, 0, 0)
        self.assertEqual(p.action_cost(state,"up",state2), 1)

        



if __name__ == "__main__":
    unittest.main()
