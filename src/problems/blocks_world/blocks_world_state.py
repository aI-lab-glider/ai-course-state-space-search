from __future__ import annotations
from typing import List, Tuple, Sequence
from base import State
from dataclasses import dataclass

@dataclass(eq=True)
class BlocksWorldState(State):
    columns: List[List[str]]

    @staticmethod
    def from_str(raw_state: str) -> BlocksWorldState:
        return BlocksWorldState([c.strip().split(',') if c.strip() != '' else [] for c in raw_state.split(";")])

    def __str__(self) -> str:
        output = "\n"
        height = max([len(c) for c in self.columns])
        for h in range(height - 1, -1, -1):
            output += " "
            row = [col[h] if len(col) > h else " " 
                   for col in self.columns]
            output += " ".join(row)
            output += " \n"
        output += "-" * 2 * len(self.columns)
        return output

    def __hash__(self) -> int:
        return tuple((tuple(c) for c in self.columns)).__hash__()
