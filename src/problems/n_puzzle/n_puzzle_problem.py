from base import Problem
from problems.n_puzzle import NPuzzleState
from typing import Union, List
from copy import deepcopy


class NPuzzleProblem(Problem):
    def __init__(self, initial: NPuzzleState, goal: NPuzzleState = None):
        super().__init__(initial,goal)

    def actions(self, state: NPuzzleState) -> List[Union[str, int]]:
        # Zwróć wszystkie możliwe akcje do wykonania z podanego stanu.
        pass


    def transition_model(self, state: NPuzzleState, action: Union[str, int]) -> NPuzzleState:
        # Z podanego stanu wykonaj akcję. Zwróć nowy stan po wykonaniu akcji.
        pass


    def action_cost(self, state:NPuzzleState, action: Union[str, int], next_state:NPuzzleState) -> int:
        # Funkcja kosztu. Jeśli takowa jest potrzebna. | return 1
        pass


    def is_goal(self, state: NPuzzleState) -> bool:
        # Przyrównaj aktalny stan problemu z oczekiwanym końcowym.
        pass


    def valid(self, x: int, y: int, nx: int, ny: int) -> bool:
        # Możesz napisać inne przydatne funkcje.
        pass