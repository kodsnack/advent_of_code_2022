#!/usr/bin/env python3

# Day 10: Cathode-Ray Tube
# By Jakob Ruhe 2022-12-10

import os
import unittest


def parse_input(input):
    return input.strip().split("\n")


def calc_x(entries):
    x_hist = [1]
    for entry in entries:
        if entry == "noop":
            x_hist.append(x_hist[-1])
        elif entry.startswith("addx "):
            x_hist.append(x_hist[-1])
            add = int(entry.split(" ")[1])
            x_hist.append(x_hist[-1] + add)
        else:
            raise ValueError(entry)
    return x_hist


def solve1(entries):
    x_hist = calc_x(entries)
    cycles = tuple(range(20, 220 + 1, 40))
    return sum([x_hist[c - 1] * c for c in cycles])


def solve2(entries):
    x_hist = calc_x(entries)
    for y in range(6):
        row = []
        for x in range(40):
            i = y * 40 + x
            row.append("#" if abs(x_hist[i] - x) <= 1 else ".")
        print("".join(row))


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input1 = """
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input1)), 13140)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input1)), None)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    solve2(entries)
