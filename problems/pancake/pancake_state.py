from base import State
from typing import List
from dataclasses import dataclass


@dataclass
class PancakeState(State):
    pancakes: List[int]

    def __hash__(self) -> int:
        return hash(tuple(self.pancakes))

    def __str__(self) -> str:
        return " ".join([str(pancake) for pancake in self.pancakes])
