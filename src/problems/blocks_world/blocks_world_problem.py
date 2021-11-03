from __future__ import annotations
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

    @staticmethod
    def deserialize(text: str) -> BlocksWorldProblem:
        def get_col(line: str) -> List[str]:
            return line[1:].strip().split()

        lines = text.splitlines()
        initial = []
        for l in lines:
            if not l.startswith('|'):
                break 
            initial.append(get_col(l))
        
        goal = []
        for l in lines[len(initial) + 1:]:
            if not l.startswith('|'):
                break
            goal.append(get_col(l))

        assert len(initial) == len(goal), \
            f"the goal and initial state should have the same number of cols"
        
        init_objects = set.union(*[set(c) for c in initial])
        goal_objects = set.union(*[set(c) for c in goal])

        assert init_objects == goal_objects, \
            "the goal and initial state should have exactly the same blocks"

        return BlocksWorldProblem(BlocksWorldState(initial), BlocksWorldState(goal))

