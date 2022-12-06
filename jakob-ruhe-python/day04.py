#!/usr/bin/env python3

# Camp Cleanup
# By Jakob Ruhe 2022-12-04

import os
import unittest
import utils


def parse_input(input):
    return input.strip().split("\n")


def contains(a, b):
    return ((a[0] <= b[0] and a[1] >= b[1]) or
            (b[0] <= a[0] and b[1] >= a[1]))


def solve1(entries):
    total = 0
    for ee in entries:
        e = utils.parse_unsigned_ints(ee)
        if contains((e[0], e[1]), (e[2], e[3])):
            total += 1
    return total


def overlaps(a, b):
    return ((a[0] <= b[1] and a[1] >= b[0]) or
            (b[0] <= a[1] and b[1] >= a[0]))


def solve2(entries):
    total = 0
    for ee in entries:
        e = utils.parse_unsigned_ints(ee)
        if overlaps((e[0], e[1]), (e[2], e[3])):
            total += 1
    return total


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 2)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 4)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
