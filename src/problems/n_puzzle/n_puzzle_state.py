from base import State
from typing import List


class NPuzzleState(State):
    def __init__(self, matrix: List[List], x: int, y: int):
        super().__init__()
        # Zdefiniuj stan problemu. Wymyśl sposób w jaki chcesz przechowywać aktualny stan problemu. Będzie to pojedynczy węzeł w całym grafie.
    
    def __hash__(self):
        # Napisz funkcję haszującą. Pamiętaj, żeby obiekt mógł być haszowany to musi być niemutowalny.
        pass

    def __str__(self) -> str:
        # Napisz funkcję, która będzie reprezentowała twój stan.
        pass

    
    def display(self):
        # print(f"void coordinates: {self.x} {self.y}")
        pass
    
    def __eq__(self, other):
        # Możesz napisać dodatkowe funkcje pomocnicze.
        pass