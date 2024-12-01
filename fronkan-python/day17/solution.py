from abc import abstractmethod
from pathlib import Path

from dataclasses import dataclass, field
from typing import Iterable, NamedTuple
from itertools import cycle, islice

# from rich import print

from aoc_lib.debugging import printer


def puzzle1(input_file: Path):
    world = Map()
    res = []
    for _ in simulate(input_file, 2023, world):
        res.append(_)
        pass
    return world.tower_height


def puzzle2(input_file: Path):
    tot_num_simulations = 1_000_000_000_000
    tower_deltas = [tower_delta for tower_delta in simulate(input_file, 50_000, Map())]
    
    for seq_len in range(5, 5001, 5):
        repeat_count = 0
        repeat_start = 0
        for step in range(0, len(tower_deltas) // seq_len):
            window_start = step * seq_len
            cur_window = tower_deltas[window_start : window_start + seq_len]
            next_window = tower_deltas[
                window_start + seq_len : window_start + (seq_len * 2)
            ]
            if cur_window == next_window:
                repeat_count += 1
                if repeat_count == 1:
                    repeat_start = step*seq_len
            else:
                repeat_count = 0

            if repeat_count == 10:
                repeating_seq = tower_deltas[repeat_start:repeat_start+seq_len]
                height_before_repeat = sum(tower_deltas[:repeat_start])
                height_from_repeating = sum(repeating_seq)*((tot_num_simulations-repeat_start)//seq_len)
                num_elements_in_last_partial_repeat = (tot_num_simulations-repeat_start)%seq_len
                height_final_partial_repeat = sum(repeating_seq[:num_elements_in_last_partial_repeat])
                return sum([height_before_repeat, height_from_repeating, height_final_partial_repeat])
                

def simulate(input_file: Path, num_blocks: int, world: "Map"):
    winds = cycle(input_file.read_text().strip())
    for idx, block_factory in enumerate(box_factory_factory(), start=1):
        prev_tower_height = world.tower_height
        if idx % 100_000 == 0:
            print(idx)
        if idx == num_blocks:
            break
        block = block_factory(world.start_position)
        while True:
            wind = next(winds)
            wind_movement = 1 if wind == ">" else -1
            block.move_x(wind_movement)
            if not world.is_allowed(block):
                block.move_x(-wind_movement)

            block.move_down()
            if not world.is_allowed(block):
                block.move_up()
                world.add_block(block.points)
                break
        yield world.tower_height - prev_tower_height


class Block:
    def __init__(
        self,
        min_x: int,
        max_x: int,
        min_y: int,
    ) -> None:
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y

    def move_down(self, steps=1):
        self.min_y -= steps

    def move_left(self, steps=1):
        self.min_x -= steps
        self.max_x -= steps

    def move_right(self, steps=1):
        self.min_x += steps
        self.max_x += steps

    def move_x(self, steps: int):
        self.min_x += steps
        self.max_x += steps

    def move_up(self, steps: int = 1):
        self.min_y += 1

    @property
    @abstractmethod
    def points(self) -> set["Point"]:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            + f"min_x={self.min_x}, "
            + f"max_x={self.max_x}, "
            + f"min_y={self.min_y}, "
            + f"points={self.points}"
            + ")"
        )


class HorizontalBlock(Block):
    @property
    def points(self):
        return {Point(self.min_x + i, self.min_y) for i in range(4)}


class CrossBlock(Block):
    @property
    def points(self):
        return {
            Point(self.min_x + 1, self.min_y),
            Point(self.min_x, self.min_y + 1),
            Point(self.min_x + 1, self.min_y + 1),
            Point(self.min_x + 2, self.min_y + 1),
            Point(self.min_x + 1, self.min_y + 2),
        }


class LBlock(Block):
    @property
    def points(self):
        return {
            *(Point(self.min_x + i, self.min_y) for i in range(3)),
            *(Point(self.min_x + 2, self.min_y + i) for i in range(1, 3)),
        }


class VerticalBlock(Block):
    @property
    def points(self):
        return {Point(self.min_x, self.min_y + i) for i in range(4)}


class BoxBlock(Block):
    @property
    def points(self):
        return {
            *(Point(self.min_x + j, self.min_y + i) for i in range(2) for j in range(2))
        }


class Point(NamedTuple):
    x: int
    y: int

    def new_move_down(self, steps=1):
        return Point(self.x, self.y - steps)

    def new_move_left(self, steps=1):
        return Point(self.x - steps, self.y)

    def new_move_right(self, steps=1):
        return Point(self.x + steps, self.y)


def box_factory_factory():
    while True:
        yield _new_horizontal
        yield _new_cross
        yield _new_L_shape
        yield _new_vertical
        yield _new_box


def _new_horizontal(start_pos: Point):
    return HorizontalBlock(min_x=start_pos.x, max_x=start_pos.x + 3, min_y=start_pos.y)


def _new_cross(start_pos: Point):
    return CrossBlock(min_x=start_pos.x, max_x=start_pos.x + 2, min_y=start_pos.y)


def _new_L_shape(start_pos: Point):
    return LBlock(min_x=start_pos.x, max_x=start_pos.x + 2, min_y=start_pos.y)


def _new_vertical(start_pos: Point):
    return VerticalBlock(min_x=start_pos.x, max_x=start_pos.x, min_y=start_pos.y)


def _new_box(start_pos: Point):
    return BoxBlock(min_x=start_pos.x, max_x=start_pos.x + 1, min_y=start_pos.y)


@dataclass
class Map:
    width: int = 7
    blocked_points: set[Point] = field(default_factory=set)
    tower_height: int = 0

    @property
    def start_position(self):
        y = self.tower_height + 3
        x = 2
        return Point(x, y)

    def is_allowed(self, block: Block):
        if block.max_x >= 7 or block.min_x < 0:
            return False
        if block.min_y > self.tower_height:
            return True
        for point in block.points:
            if not (0 <= point.x < 7):
                return False
            if point.y < 0:
                return False
            if point in self.blocked_points:
                return False
        return True

    def add_block(self, block: set[Point]):
        block_height = max(point.y for point in block) + 1
        if block_height > self.tower_height:
            self.tower_height = block_height
        self.blocked_points |= block

    def render_with_falling_block(self, block: set[Point]):
        import numpy as np

        map = np.zeros((self.start_position.y + 5, 7), dtype=np.int8)

        for point in block:
            map[point.y, point.x] = 2

        for point in self.blocked_points:
            map[point.y, point.x] = 1

        print("\n".join(["".join(str(c) for c in row) for row in np.flipud(map)]))

    def render(self):
        import numpy as np

        map = np.zeros((self.tower_height + 1, 7), dtype=np.int8)
        for point in self.blocked_points:
            map[point.y, point.x] = 1
        print("\n".join(["".join(str(c) for c in row) for row in np.flipud(map)]))


if __name__ == "__main__":
    print("Day 17")
    input_file = Path(__file__).parent / "input.txt"
    # input_file = Path(__file__).parent / "example_input.txt"
    print("Puzzle 1:", puzzle1(input_file))
    print("Puzzle 2:", puzzle2(input_file))
