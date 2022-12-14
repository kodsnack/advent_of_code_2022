#!/usr/bin/env python3
#
# Day 13: Distress Signal
# By Jakob Ruhe 2022-12-13

import os
import unittest
from functools import cmp_to_key

LIST_START = "["
LIST_END = "]"
SEP = ","


def parse_input(input):
    return input.strip().split("\n\n")


def find_end_of_list(string, start):
    depth = 0
    i = start
    while True:
        if string[i] == LIST_START:
            depth += 1
        elif string[i] == LIST_END:
            depth -= 1
            if depth == 0:
                break
        i += 1
    return i


def parse_number(string, start):
    i = start
    while string[i].isdigit():
        i += 1
    return int(string[start:i]), i


def parse_list(string):
    result = []
    assert string[0] == LIST_START
    i = 1
    while i < len(string) - 1:
        if string[i] == LIST_START:
            sub_list_start = i
            i = find_end_of_list(string, i) + 1
            result.append(parse_list(string[sub_list_start:i]))
        elif string[i] == LIST_END:
            assert i == 1
            # Empty list
            break
        elif string[i].isdigit():
            number, i = parse_number(string, i)
            result.append(number)
        elif string[i] == SEP:
            i += 1
        else:
            raise ValueError("Unexpected character: " + string[i])
    assert string[i] == LIST_END
    return result


def compare(left, right, depth=0):
    if isinstance(left, int) and isinstance(right, int):
        return -1 if left < right else 1 if left > right else 0
    elif isinstance(left, list) and isinstance(right, list):
        min_len = min(len(left), len(right))
        for i in range(min_len):
            c = compare(left[i], right[i], depth + 1)
            if c != 0:
                return c
        return -1 if len(left) < len(right) else 1 if len(left) > len(right) else 0
    elif isinstance(left, list) and isinstance(right, int):
        return compare(left, [right])
    elif isinstance(left, int) and isinstance(right, list):
        return compare([left], right)
    else:
        raise ValueError(f"Cannot compare: {left} and {right}")


def solve1(pairs):
    right_order = []
    for k, v in enumerate(pairs):
        left, right = v.split("\n")
        if compare(parse_list(left), parse_list(right)) <= 0:
            right_order.append(k + 1)
    return sum(right_order)


def solve2(pairs):
    divider_packet1 = [[2]]
    divider_packet2 = [[6]]
    all_lists = [divider_packet1, divider_packet2]
    for pair in pairs:
        left, right = pair.split("\n")
        all_lists.append(parse_list(left))
        all_lists.append(parse_list(right))
    sorted_lists = sorted(all_lists, key=cmp_to_key(compare))
    i1 = sorted_lists.index(divider_packet1) + 1
    i2 = sorted_lists.index(divider_packet2) + 1
    return i1 * i2


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 13)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 140)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
