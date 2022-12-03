#!/usr/bin/env python3

# Rucksack Reorganization
# By Jakob Ruhe 2021-12-03

import os
import utils
import unittest


def parse_input(input):
    return input.strip().split("\n")


def find_common_letter(items):
    for c in items[0]:
        can_be_common = True
        for item in items[1:]:
            if c not in item:
                can_be_common = False
                break
        if can_be_common:
            return c


def points_for_letter(letter):
    return (
        ord(letter) - ord("A") + 27 if letter.isupper() else
        ord(letter) - ord("a") + 1
    )


def solve1(entries):
    total = 0
    for e in entries:
        assert len(e) % 2 == 0
        half = len(e) // 2
        group = (e[:half], e[-half:])
        common = find_common_letter(group)
        assert common is not None
        total += points_for_letter(common)
    return total


def solve2(entries):
    groups = utils.split_into_groups(entries, 3)
    total = 0
    for group in groups:
        common = find_common_letter(group)
        assert common is not None
        total += points_for_letter(common)
    return total


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 157)
        pass

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 70)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
