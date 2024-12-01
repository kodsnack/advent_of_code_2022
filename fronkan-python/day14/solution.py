from pathlib import Path
from typing import cast

import numpy as np
from collections import deque


def puzzle1(input_file: Path):
    max_row, max_col, all_points = parse_input(input_file)
    cave = np.zeros((max_row + 1, max_col + 1), dtype=np.int8)
    for point in all_points:
        cave[point] = 1

    void = False
    while not void:
        rest = False
        sand = (0, 500)
        while not void and not rest:
            # flow down
            if not _is_in_bounds(sand, (max_row - 1, max_col - 1)):
                void = True
                break
            for op in [flow_down, flow_diag_left, flow_diag_right]:
                new_sand = op(sand, cave)
                if new_sand != sand:
                    sand = new_sand
                    break
            else:
                rest = True
                cave[sand] = 2

        # print(*["".join(str(c) for c in row) for row in cave[:,490:]], sep="\n")

    return np.sum(cave == 2)


def puzzle2(input_file: Path):
    max_row, max_col, all_points = parse_input(input_file)
    cave = np.zeros((max_row + 4, max_col*3), dtype=np.int8)
    for point in all_points:
        cave[point] = 1

    cave[max_row+2, :] = 1

    void = False
    while not void:
        rest = False
        sand = (0, 500)
        while not void and not rest:
            # flow down
            if not _is_in_bounds(sand, cave.shape):
                raise RuntimeError(f"{sand=}, {max_row=}, {max_col=}")
            
            for op in [flow_down, flow_diag_left, flow_diag_right]:
                new_sand = op(sand, cave)
                if new_sand != sand:
                    sand = new_sand
                    break
            else:
                rest = True
                cave[sand] = 2
                if sand == (0, 500):
                    void = True

        # print(*["".join(str(c) for c in row) for row in cave[:,490:]], sep="\n")

    return np.sum(cave == 2)

def flow_down(sand: tuple[int, int], cave: np.ndarray) -> tuple[int, int]:
    row_delta = cast(int, np.argmax(cave[sand[0] :, sand[1]] != 0) - 1)
    if row_delta != -1:
        return (sand[0] + row_delta, sand[1])
    return sand


def flow_diag_left(sand: tuple[int, int], cave: np.ndarray) -> tuple[int, int]:
    new_sand = (sand[0] + 1, sand[1] - 1)
    if not _is_in_bounds(new_sand, cave.shape):
        return sand
    if cave[new_sand] == 0:
        return new_sand
    return sand


def flow_diag_right(sand: tuple[int, int], cave: np.ndarray) -> tuple[int, int]:
    new_sand = (sand[0] + 1, sand[1] + 1)
    if not _is_in_bounds(new_sand, cave.shape):
        return sand
    if cave[new_sand] == 0:
        return new_sand
    return sand


def _is_in_bounds(point, upper_boundary):
    if point[0] < 0 or point[1] < 0:
        return False
    if point[0] > upper_boundary[0] or point[1] > upper_boundary[1]:
        return False
    return True


def parse_input(input_file: Path):
    all_points = deque()
    max_row = 0
    min_row = 10000000
    max_col = 0
    min_col = 10000000
    for row in input_file.read_text().splitlines():
        points = [
            np.flip(np.array([int(e) for e in point.split(",")]))
            for point in row.split("->")
        ]
        start_point = points[0]
        for end_point in points[1:]:
            for point in draw_straight_line(start_point, end_point, include_end=True):
                all_points.append(point)
                if point[0] > max_row:
                    max_row = point[0]
                elif point[0] < min_row:
                    min_row = point[0]
                if point[1] > max_col:
                    max_col = point[1]
                elif point[1] < min_col:
                    min_col = point[1]
            start_point = end_point
    return max_row, max_col, all_points


def draw_straight_line(start_point, end_point, include_end=False):
    if start_point[0] == end_point[0]:
        end = end_point[1]
        start = start_point[1]
        direction = -1 if end <= start else 1

        if include_end:
            end = end + direction

        for p in range(start, end, direction):
            yield (start_point[0], p)

    elif start_point[1] == end_point[1]:
        end = end_point[0]
        start = start_point[0]
        direction = -1 if end <= start else 1

        if include_end:
            end = end + direction

        for p in range(start, end, direction):
            yield (p, start_point[1])

    else:
        raise ValueError(f"{start_point=}, {end_point=}")


if __name__ == "__main__":
    print("Day 14")
    input_file = Path(__file__).parent / "input.txt"
    # input_file = Path(__file__).parent / "example_input.txt"
    print("Puzzle 1:", puzzle1(input_file))
    print("Puzzle 2:", puzzle2(input_file))
