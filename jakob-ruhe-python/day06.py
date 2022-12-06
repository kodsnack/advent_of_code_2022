#!/usr/bin/env python3

# Tuning Trouble
# By Jakob Ruhe 2022-12-06

import os
import unittest


def parse_input(input):
    return input.strip()


def all_unique(marker):
    return len(set(marker)) == len(marker)


def find_marker(text, marker_len):
    for i in range(len(text) - marker_len + 1):
        marker = text[i : i + marker_len]
        if all_unique(marker):
            return i + marker_len


def solve1(text):
    return find_marker(text, 4)


def solve2(text):
    return find_marker(text, 14)


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 7)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 19)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
