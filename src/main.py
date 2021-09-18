
from typing import final
from problems import NPuzzleProblem
from solvers import BFS
from state import NPuzzleState


if __name__ == '__main__':
    
    start_matrix = [[0,2,3], [1,4,5], [8,7,6]]
    final_matrix = [[0,1,2], [3,4,5], [6,7,8]]

    start_state = NPuzzleState(start_matrix, 0, 0)
    final_state = NPuzzleState(final_matrix, 0, 0)

    p = NPuzzleProblem(start_state, final_state)
    
    print(p.is_goal(final_state))
    
    """
    s = BFS(p,start_state)
    
    s.run()
    """
    
