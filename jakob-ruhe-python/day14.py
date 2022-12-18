#!/usr/bin/env python3

# Day 14: Regolith Reservoir
# By Jakob Ruhe 2022-12-14

import os
import unittest
from utils import parse_ints, Point


def parse_input(input):
    return input.strip().split("\n")


def parse_stones(entries):
    segments = []
    for row in entries:
        p = parse_ints(row)
        points = [Point(p[i], p[i + 1]) for i in range(0, len(p), 2)]
        segments.append(points)
    stones = set()
    for points in segments:
        for i in range(len(points) - 1):
            draw_line(stones, points[i], points[i + 1])
    return stones


def draw_line(pixels, start, end):
    dx = end.x - start.x
    dy = end.y - start.y
    # Line must be horizontal or vertical.
    assert dx == 0 or dy == 0
    ddx = 1 if dx > 0 else -1 if dx < 0 else 0
    ddy = 1 if dy > 0 else -1 if dy < 0 else 0
    p = start
    pixels.add(p)
    while p != end:
        p = Point(p.x + ddx, p.y + ddy)
        pixels.add(p)


def drop_sand(source, stones, sand, y_max):
    stones_or_sand = stones | sand
    p = source
    while p.y < y_max:
        p_down = Point(p.x, p.y + 1)
        p_down_left = Point(p.x - 1, p.y + 1)
        p_down_right = Point(p.x + 1, p.y + 1)
        if p_down not in stones_or_sand:
            p = p_down
        elif p_down_left not in stones_or_sand:
            p = p_down_left
        elif p_down_right not in stones_or_sand:
            p = p_down_right
        else:
            break
    return p


def solve1(entries):
    stones = parse_stones(entries)
    sand = set()
    y_max = max([p.y for p in stones])
    source = Point(500, 0)
    while True:
        p = drop_sand(source, stones, sand, y_max)
        if p.y >= y_max:
            break
        sand.add(p)
    return len(sand)


def solve2(entries):
    stones = parse_stones(entries)
    sand = set()
    y_max = max([p.y for p in stones])
    source = Point(500, 0)
    while True:
        p = drop_sand(source, stones, sand, y_max + 1)
        sand.add(p)
        if p.y == source.y:
            break
    return len(sand)


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 24)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 93)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
