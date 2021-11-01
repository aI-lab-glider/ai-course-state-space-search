from typing import List
from base import Problem
from problems.blocks_world.blocks_world_action import BlocksWorldAction
from problems.blocks_world.blocks_world_state import BlocksWorldState

class BlocksWorldProblem(Problem[BlocksWorldState, BlocksWorldAction]):
    def __init__(self, initial: BlocksWorldState, goal: BlocksWorldState):
        super().__init__(initial)
        self.goal = goal

    def actions(self, state: BlocksWorldState) -> List[BlocksWorldAction]:
        non_empty_columns = [i for i,c in enumerate(state.columns) if len(c) > 0]
        columns = range(len(state.columns))

        return [ BlocksWorldAction(col_from, col_to)
            for col_from in non_empty_columns
            for col_to in columns
            if col_from != col_to
        ]

    def take_action(self, state: BlocksWorldState, action: BlocksWorldAction) -> BlocksWorldState:
        return action.apply(state)

    def action_cost(self, s: BlocksWorldState, a: BlocksWorldAction, e: BlocksWorldState) -> int:
        return 1

    def is_goal(self, state: BlocksWorldState) -> bool:
        return state == self.goal