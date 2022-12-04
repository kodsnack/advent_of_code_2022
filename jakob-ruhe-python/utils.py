#!/usr/bin/env python3

# Random utility functions by Jakob Ruhe

import unittest
import re

DIRS = ("N", "W", "S", "E")


def dir_from_name(name):
    return DIRS.index(name)


def dir_name(d):
    return DIRS[d]


def dir_x(d):
    return (0, -1, 0, 1)[d]


def dir_y(d):
    return (1, 0, -1, 0)[d]


def turn_left(d):
    return (d + 1) % len(DIRS)


def turn_right(d):
    return (d - 1) % len(DIRS)


def split_into_groups(items, group_size):
    num = len(items)
    if num % group_size != 0:
        raise ValueError(f"# items ({num}) is not a multiple of {group_size}")
    return [items[i : i + group_size] for i in range(0, num, group_size)]


def parse_ints(string):
    groups = re.findall(r"-?\d+", string)
    return tuple(map(int, groups))


def parse_unsigned_ints(string):
    groups = re.findall(r"\d+", string)
    return tuple(map(int, groups))


# Execute tests with:
# python3 -m unittest utils
class TestThis(unittest.TestCase):
    def test_dir(self):
        self.assertEqual(turn_left(dir_from_name("N")), dir_from_name("W"))
        self.assertEqual(turn_left(dir_from_name("W")), dir_from_name("S"))
        self.assertEqual(turn_left(dir_from_name("S")), dir_from_name("E"))
        self.assertEqual(turn_left(dir_from_name("E")), dir_from_name("N"))
        self.assertEqual(turn_right(dir_from_name("N")), dir_from_name("E"))
        self.assertEqual(turn_right(dir_from_name("W")), dir_from_name("N"))
        self.assertEqual(turn_right(dir_from_name("S")), dir_from_name("W"))
        self.assertEqual(turn_right(dir_from_name("E")), dir_from_name("S"))

    def test_split_into_groups(self):
        self.assertEqual(split_into_groups((1, 2, 3, 4), 2), [(1, 2), (3, 4)])
        with self.assertRaises(ValueError):
            split_into_groups((1, 2, 3, 4), 3)

    def test_parse_ints(self):
        self.assertEqual(parse_ints(""), ())
        self.assertEqual(parse_ints("no digits"), ())
        self.assertEqual(parse_ints("123"), (123,))
        self.assertEqual(parse_ints("123,-456,789"), (123, -456, 789))
        self.assertEqual(parse_ints("hello12,3world 4567."), (12, 3, 4567))

    def test_parse_unsigned_ints(self):
        self.assertEqual(parse_unsigned_ints(""), ())
        self.assertEqual(parse_unsigned_ints("no digits"), ())
        self.assertEqual(parse_unsigned_ints("123,-456,789"), (123, 456, 789))
        self.assertEqual(parse_unsigned_ints("2-6,4-8"), (2, 6, 4, 8))
