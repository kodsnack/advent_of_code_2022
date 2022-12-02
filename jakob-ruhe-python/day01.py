#!/usr/bin/env python3

# By Jakob Ruhe 2021-12-01

import os
import unittest


def parse_input(input):
    return input.strip().split("\n\n")


def sum_of_groups(groups):
    sums = [sum(map(int, g.split("\n"))) for g in groups]
    return sorted(sums, reverse=True)


def solve1(groups):
    return sum_of_groups(groups)[0]


def solve2(groups):
    return sum(sum_of_groups(groups)[:3])


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 24000)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 45000)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
