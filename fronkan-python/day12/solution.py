from collections import deque
from pathlib import Path
from string import ascii_lowercase

import numpy as np

from aoc_lib.np_grid import manhattan_neighbors

HEIGHTS = {
    letter: height
    for height, letter in enumerate(ascii_lowercase)
}
HEIGHTS["S"] = 0
HEIGHTS["E"] = max(HEIGHTS.values())

def puzzle1(input_file: Path):
    map = Map.from_string(input_file.read_text())
    visited = set()
    to_visit = deque([(map.start, [])])
    prev_positions = []
    while to_visit:
        cur_position, prev_positions = to_visit.popleft()
        cur_height = map.heights[cur_position]
        if cur_position == map.goal:
            return len(prev_positions)
        visited.add(cur_position)
        cur_row, cur_col = cur_position
        neighbors = manhattan_neighbors(map.heights, cur_row, cur_col)
        directions = np.where(neighbors <= cur_height +1)[0]
        # print(cur_position, cur_height, neighbors, directions)
        for direction in directions:
            new_pos = _pos_from_direction(cur_row, cur_col, direction)
            if new_pos not in visited:
                visited.add(new_pos)
                # print("new:", new_pos, map.heights[new_pos])
                to_visit.append((new_pos, [*prev_positions, cur_position]))
    
    raise RuntimeError("Couldn't find a goal")

def _pos_from_direction(cur_row: int, cur_col: int, direction: int):
    if direction == 0:
        new_pos = (cur_row,cur_col-1)
    elif direction == 1:
        new_pos = (cur_row+1, cur_col)
    elif direction == 2:
        new_pos = (cur_row, cur_col+1)
    elif direction == 3:
        new_pos = (cur_row-1, cur_col)
    else: 
        raise ValueError(f"{direction=}")
    return new_pos
    
class Map:
    def __init__(self, start: tuple[int, int], goal: tuple[int, int], heights: np.ndarray):
        self.start = start
        self.goal = goal
        self.heights = heights

    @classmethod
    def from_string(cls, map_data: str, padding_value=100):
        start = (-1,-1)
        goal = (-1,-1)
        map_rows = []
        for row, line in enumerate(map_data.splitlines()):
            map_row = []
            for col, char in enumerate(line):
                if char == "S":
                    start = (row+1, col+1)
                if char == "E":
                    goal = (row+1, col+1)
                map_row.append(HEIGHTS[char])
            map_rows.append(map_row)
        map = np.array(map_rows)
        map = np.pad(map, 1, constant_values=padding_value)
        return cls(start, goal, map)

            
        



def puzzle2(input_file: Path):
    map = Map.from_string(input_file.read_text(), padding_value=-100)
    visited = set()
    to_visit = deque([(map.goal, [])])
    prev_positions = []
    while to_visit:
        cur_position, prev_positions = to_visit.popleft()
        cur_height = map.heights[cur_position]
        if cur_height == 0:
            return len(prev_positions)
        visited.add(cur_position)
        cur_row, cur_col = cur_position
        neighbors = manhattan_neighbors(map.heights, cur_row, cur_col)
        directions = np.where((neighbors == cur_height -1) | (neighbors >= cur_height))[0]
        # print(cur_position, cur_height, neighbors, directions)
        for direction in directions:
            new_pos = _pos_from_direction(cur_row, cur_col, direction)
            if new_pos not in visited:
                visited.add(new_pos)
                # print("new:", new_pos, map.heights[new_pos])
                to_visit.append((new_pos, [*prev_positions, cur_position]))

    raise RuntimeError("Couldn't find a goal")

if __name__ == "__main__":
    print("Day 12")
    input_file = Path(__file__).parent / "input.txt"
    # input_file = Path(__file__).parent / "example_input.txt"
    print("Puzzle 1:", puzzle1(input_file))
    print("Puzzle 2:", puzzle2(input_file))