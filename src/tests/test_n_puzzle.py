import unittest
from src.problems.n_puzzle import NPuzzleProblem
from src.problems.n_puzzle import NPuzzleState



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
        p = NPuzzleProblem(state)   # goal = None

        self.assertEqual(p.actions(state),["down", "up", "right"])



        
    


if __name__ == "__main__":
    unittest.main()
