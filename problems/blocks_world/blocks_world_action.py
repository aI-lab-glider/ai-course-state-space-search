from dataclasses import dataclass
from problems.blocks_world.blocks_world_state import BlocksWorldState
from copy import deepcopy

@dataclass
class BlocksWorldAction:
    column_from: int
    column_to: int

    def apply(self, state: BlocksWorldState) -> BlocksWorldState:
        # TODO:
        # - create a new state by applying the action
        #   (move block from 'self.column_from' to 'self.column_to')
        # tip. remember to not modify the current state!
        new_columns = deepcopy(state.columns)
        new_columns[self.column_to].append(new_columns[self.column_from].pop())
        return BlocksWorldState(new_columns)
    
    def __str__(self) -> str:
        return f"move block from col: {self.column_from} to col: {self.column_to}"
