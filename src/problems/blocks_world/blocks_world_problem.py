from __future__ import annotations
from typing import List, Tuple
from base import Problem
from problems.blocks_world.blocks_world_action import BlocksWorldAction
from problems.blocks_world.blocks_world_state import BlocksWorldState
from PIL import Image, ImageDraw, ImageFont

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
    
    def to_image(self, state: BlocksWorldState, size: Tuple[int, int] = (800, 800)) -> Image.Image:
        state_img = Image.new('RGB', size, color=(248, 255, 229))
        padding_top = 0.1 * state_img.height
        container_shape = state_img.width // len(state.columns), int(state_img.height - padding_top) // max(len(col) for col in self.goal.columns) 
        
        for j, col in enumerate(reversed(state.columns)):
            for i, block_name in enumerate(col):
                block_img = self._create_block_image(container_shape, block_name)
                x_start = block_img.width * j
                y_start = i * block_img.height
                state_img.paste(block_img, (x_start, y_start), mask=block_img)
                
        return state_img.rotate(180)

    def _create_block_image(self, container_shape, name) -> Image.Image:
        block_img = Image.new('RGBA', container_shape, (0,0,0,0))
        block_draw = ImageDraw.Draw(block_img)
        (container_width, container_height) = container_shape
        (block_width, block_height) = min(container_shape), min(container_shape)
        font = ImageFont.truetype("arial.ttf", size=int(0.8 * block_height))
        
        def apply_padding(corner: Tuple[int, int]):
            x, y = corner
            padding = (max(container_shape) - block_width) // 2
            x = x + padding if x == 0 else x - padding
            return (x, y)
        
        corners = list(map(apply_padding, [(0, 0), (block_img.width, 0), (block_img.width, block_img.height), (0, block_img.height)]))
        
        for from_corner, to_corner in zip(corners, corners[1:] + [corners[0]]):
            block_draw.line((from_corner, to_corner), fill='black', width=3)    
        block_draw.text((
                container_width // 2,
                container_height // 2
            ), name, fill='black', font=font, anchor='mm')
        block_img = block_img.rotate(180)
        return block_img


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