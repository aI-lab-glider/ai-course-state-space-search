from __future__ import annotations
from pathlib import Path

from PIL import Image
from base import Problem
from base.problem import ReversibleProblem
from problems.n_puzzle import NPuzzleState
from typing import List, Tuple, Set
from copy import deepcopy

from problems.n_puzzle.n_puzzle_action import NPuzzleAction


class NPuzzleProblem(ReversibleProblem[NPuzzleState, NPuzzleAction]):

    def __init__(self, initial: NPuzzleState, goal: NPuzzleState):
        super().__init__(initial, goal)

    def actions(self, state: NPuzzleState) -> List[NPuzzleAction]:
        return [shift for shift in NPuzzleAction
                if self.valid(state.x + shift.value[0],
                              state.y + shift.value[1],
                              state.nx, state.ny)]

    def take_action(self, state: NPuzzleState, action: NPuzzleAction) -> NPuzzleState:
        shift_x, shift_y = action.value
        if self.valid(state.x+shift_x, state.y+shift_y, state.nx, state.ny):
            state2 = deepcopy(state)
            state2.matrix[state2.x][state2.y] = state2.matrix[state2.x +
                                                              shift_x][state2.y+shift_y]
            state2.matrix[state2.x+shift_x][state2.y +
                                            shift_y] = state.matrix[state.x][state.y]
            state2.x = state2.x + shift_x
            state2.y = state2.y + shift_y
            return state2

        raise Exception("Illegal action")

    def action_cost(self, state: NPuzzleState, action: NPuzzleAction, next_state: NPuzzleState) -> float:
        return 1

    def is_goal(self, state: NPuzzleState) -> bool:
        return self.goal.matrix == state.matrix

    def reversed(self):
        return NPuzzleProblem(self.goal, self.initial)

    def valid(self, x: int, y: int, nx: int, ny: int) -> bool:
        return 0 <= x < nx and 0 <= y < ny

    def to_image(self, state: NPuzzleState, size: Tuple[int, int] = (800, 800)) -> Image.Image:
        puzzle_path = Path(__file__).parent.joinpath(
            "instances").joinpath("puzzle.jpg")
        puzzle_img = Image.open(puzzle_path)
        puzzle_img = puzzle_img.resize(size)
        chunk_size = (int(size[0] / state.nx), int(size[1] / state.ny))

        def get_offset(row: int, col: int) -> Tuple[int, int]:
            return (int(col * chunk_size[0]), int(row * chunk_size[1]))

        def get_chunk(index: int) -> Image.Image:
            row = index // state.nx
            col = index % state.nx
            offset = get_offset(row, col)

            return puzzle_img.crop((offset[0], offset[1],
                                    offset[0] + chunk_size[0],
                                    offset[1] + chunk_size[1]))

        img = Image.new("RGB", size, "lightgray")
        for r, row in enumerate(state.matrix):
            for c, cell in enumerate(row):
                if cell == 0:
                    continue
                offset = get_offset(r, c)
                chunk = get_chunk(cell - 1)
                img.paste(chunk, offset)

        return img

    @staticmethod
    def deserialize(text: str) -> NPuzzleProblem:
        def read_line(l: str) -> List[int]:
            return [int(v) for v in l.split()]

        def zero_coords(array: List[List[int]]) -> Tuple[int, int]:
            for i, row in enumerate(array):
                if 0 in row:
                    return i, row.index(0)
            assert False, "the n-puzzle state should contain 0"

        lines = text.splitlines()
        initial: List[List[int]] = []
        initial.append(read_line(lines[0]))
        size = len(initial[0])
        ix = 0 if 0 in initial[0] else -1
        iy = -1 if ix < 0 else initial[0].index(0)

        for i in range(1, size):
            initial.append(read_line(lines[i]))

        assert all([len(r) == size for r in initial]), \
            "the n-puzzle initial state should be square"

        goal: List[List[int]] = []
        for i in range(size + 1, 2*size + 1):
            goal.append(read_line(lines[i]))
        assert all([len(r) == size for r in goal]), \
            "the n-puzzle goal state should be square and the same size as initial"

        init_numbers: Set[int] = set.union(*[set(r) for r in initial])
        goal_numbers: Set[int] = set.union(*[set(r) for r in goal])

        assert init_numbers == goal_numbers, \
            "the n-puzzle init and goal states should share the same numbers"

        ix, iy = zero_coords(initial)
        gx, gy = zero_coords(goal)
        return NPuzzleProblem(NPuzzleState(initial, ix, iy), NPuzzleState(goal, gx, gy))
