#!/usr/bin/env python3

# Supply Stacks
# By Jakob Ruhe 2022-12-05

import os
import unittest
from utils import parse_ints


def parse_input(input):
    lines = input.split("\n")
    empty_line = lines.index("")

    num_stacks = len(parse_ints(lines[empty_line - 1]))

    stacks = []
    for s in range(num_stacks):
        stack = []
        pos = 1 + s * 4
        for line in lines[0 : empty_line - 1]:
            crate = line[pos] if pos < len(line) else " "
            if crate != " ":
                stack.append(crate)
        stacks.append(tuple(reversed(stack)))

    instructions = [parse_ints(line) for line in lines[empty_line + 1 :] if line]

    return tuple(stacks), tuple(instructions)


def top_of_stacks(stacks):
    return [stack[-1] for stack in stacks if stack]


def solve1(parsed_input):
    stacks_input, instructions = parsed_input
    stacks = [list(stack) for stack in stacks_input]

    for num, source, dest in instructions:
        for i in range(num):
            stacks[dest - 1].append(stacks[source - 1].pop())

    return "".join(top_of_stacks(stacks))


def solve2(parsed_input):
    stacks_input, instructions = parsed_input
    stacks = [list(stack) for stack in stacks_input]

    for num, source, dest in instructions:
        temp_storage = [stacks[source - 1].pop() for _ in range(num)]
        for crate in reversed(temp_storage):
            stacks[dest - 1].append(crate)

    return "".join(top_of_stacks(stacks))


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), "CMZ")

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), "MCD")


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
