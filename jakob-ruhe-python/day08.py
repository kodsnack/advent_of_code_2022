#!/usr/bin/env python3

# Day 8: Treetop Tree House
# By Jakob Ruhe 2022-12-08

import os
import unittest
from utils import dir_x, dir_y, dir_from_name, Point


def parse_input(input):
    return input.strip().split("\n")


def is_inside(grid, p):
    return p.x >= 0 and p.x < len(grid[0]) and p.y >= 0 and p.y < len(grid)


def next_point(p, d):
    return Point(p.x + dir_x(d), p.y + dir_y(d))


def tree(grid, p):
    return int(grid[p.y][p.x])


def look1(grid, p, d):
    visible = set()
    tallest = -1
    while is_inside(grid, p):
        t = tree(grid, p)
        if t > tallest:
            visible.add(p)
            tallest = t
        p = next_point(p, d)
    return visible


def solve1(entries):
    visible = set()

    w = len(entries[0])
    h = len(entries)

    for y in range(h):
        visible.update(look1(entries, Point(0, y), dir_from_name("R")))
        visible.update(look1(entries, Point(w - 1, y), dir_from_name("L")))

    for x in range(w):
        visible.update(look1(entries, Point(x, 0), dir_from_name("U")))
        visible.update(look1(entries, Point(x, h - 1), dir_from_name("D")))

    return len(visible)


def look2(grid, start, d):
    num = 0
    start_height = tree(grid, start)
    p = next_point(start, d)
    while is_inside(grid, p):
        num += 1
        if tree(grid, p) >= start_height:
            break
        p = next_point(p, d)
    return num


def scenic_score(grid, p):
    up = look2(grid, p, dir_from_name("U"))
    down = look2(grid, p, dir_from_name("D"))
    left = look2(grid, p, dir_from_name("L"))
    right = look2(grid, p, dir_from_name("R"))
    return up * down * left * right


def solve2(entries):
    max_score = 0
    w = len(entries[0])
    h = len(entries)

    for y in range(h):
        for x in range(w):
            score = scenic_score(entries, Point(x, y))
            max_score = max(max_score, score)

    return max_score


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
30373
25512
65332
33549
35390
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 21)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 8)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
