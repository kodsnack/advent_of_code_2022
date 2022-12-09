#!/usr/bin/env python3

# Day 9: Rope Bridge
# By Jakob Ruhe 2022-12-09

import os
import unittest
from utils import dir_from_name, dir_x, dir_y, Point


def parse_input(input):
    return input.strip().split("\n")


def move(pos, d):
    return Point(pos.x + dir_x(d), pos.y + dir_y(d))


def move_tail(head, tail):
    dx = head.x - tail.x
    dy = head.y - tail.y
    if abs(dx) <= 1 and abs(dy) <= 1:
        return tail
    else:
        sx = 1 if dx > 0 else -1 if dx < 0 else 0
        sy = 1 if dy > 0 else -1 if dy < 0 else 0
        return Point(tail.x + sx, tail.y + sy)


def solve(entries, length):
    visited = set()
    rope = []
    for _ in range(length):
        rope.append(Point(0, 0))
    visited.add(rope[-1])

    for e in entries:
        ee = e.split(" ")
        d = dir_from_name(ee[0])
        steps = int(ee[1])
        for s in range(steps):
            rope[0] = move(rope[0], d)
            for i in range(1, length):
                rope[i] = move_tail(rope[i - 1], rope[i])
            visited.add(rope[-1])

    return len(visited)


def solve1(entries):
    return solve(entries, 2)


def solve2(entries):
    return solve(entries, 10)


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 13)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 1)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
