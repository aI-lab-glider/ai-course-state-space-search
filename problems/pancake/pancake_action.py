from dataclasses import dataclass, astuple
from problems.pancake.pancake_state import PancakeState
from copy import deepcopy


@dataclass
class PancakeAction:
    flip_depth: int

    def apply(self, state: PancakeState) -> PancakeState:
        new_pancakes = deepcopy(state.pancakes)
        new_pancakes[0:self.flip_depth] = new_pancakes[0:self.flip_depth][::-1]
        return PancakeState(new_pancakes)

    def __hash__(self):
        return hash(astuple(self))
