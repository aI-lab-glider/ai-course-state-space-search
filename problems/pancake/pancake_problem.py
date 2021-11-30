from typing import List, Tuple
from base.problem import Problem
from problems.pancake.pancake_state import PancakeState
from problems.pancake.pancake_action import PancakeAction
from PIL import Image, ImageDraw


class PancakeProblem(Problem[PancakeState, PancakeAction]):
    def __init__(self, initial: PancakeState):
        super().__init__(initial)
        self.n_pancakes = len(initial.pancakes) - 1
        self.goal = PancakeState(pancakes=[i for i in range(1, self.n_pancakes+2)])

    def actions(self, state: PancakeState) -> List[PancakeAction]:
        return [PancakeAction(flip_depth=depth) for depth in range(2, self.n_pancakes+1)]

    def take_action(self, state: PancakeState, action: PancakeAction) -> PancakeState:
        return action.apply(state)

    def action_cost(self, state: PancakeState, action: PancakeAction) -> float:
        return 1

    def is_goal(self, state: PancakeState) -> bool:
        return state == self.goal

    def to_image(self, state: PancakeState, size: Tuple[int, int] = (800, 800)) -> Image.Image:
        background_color = (248, 255, 229)
        pancake_color = (236, 162, 77)
        pancake_outline = (180, 83, 38)
        plate_color = (31, 122, 140)
        image = Image.new("RGB", size, background_color)
        draw = ImageDraw.Draw(image)
        draw.rectangle((size[0] * 0.15, size[1] * 0.9, size[0] * 0.85, size[1] * 0.93), plate_color)

        size_diff = (0.7-0.25)/self.n_pancakes/2
        thickness = size[0]*0.8/self.n_pancakes

        for i in range(self.n_pancakes):
            draw.ellipse((size[0] * (0.15 + size_diff * (self.n_pancakes-state.pancakes[i])),
                          size[1] * 0.9 - thickness * (self.n_pancakes - i),
                          size[0] * (0.85 - size_diff * (self.n_pancakes-state.pancakes[i])),
                          size[1] * 0.9 - thickness * (self.n_pancakes - i - 1)),
                         pancake_color, outline=pancake_outline)
        return image

    @staticmethod
    def deserialize(text: str) -> 'PancakeProblem':
        pancakes = [int(pancake) for pancake in text.split()]
        return PancakeProblem(PancakeState(pancakes))
