#!/usr/bin/env python3

# Day 11: Monkey in the Middle
# By Jakob Ruhe 2022-12-11

import os
import unittest
from utils import parse_ints
import math


class Monkey:
    def __init__(self, name, items, op, test, if_true, if_false):
        self.name = name
        self.items = items
        self.op = op
        self.test = test
        self.if_true = if_true
        self.if_false = if_false
        self.num_inspected = 0


def parse_input(input):
    groups = input.strip().split("\n\n")
    monkies = []
    for group in groups:
        # Quick and dirty parsing.
        lines = group.strip().split("\n")
        items = list(parse_ints(lines[1]))
        op = lines[2].split("=")[1].strip()
        test = parse_ints(lines[3])[0]
        if_true = parse_ints(lines[4])[0]
        if_false = parse_ints(lines[5])[0]
        monkies.append(Monkey(len(monkies), items, op, test, if_true, if_false))
    return monkies


def make_turn(monkies, divide, modulo, m):
    while m.items:
        m.num_inspected += 1
        old = m.items.pop(0)
        item = eval(m.op)
        if divide:
            item = item // divide
        if modulo:
            item = item % modulo
        give_to = m.if_true if item % m.test == 0 else m.if_false
        monkies[give_to].items.append(item)


def monkey_business(monkies):
    top = sorted(monkies, key=lambda m: m.num_inspected, reverse=True)
    return top[0].num_inspected * top[1].num_inspected


def solve1(monkies):
    for r in range(20):
        for m in monkies:
            make_turn(monkies, 3, 0, m)
    return monkey_business(monkies)


def solve2(monkies):
    divisors = [m.test for m in monkies]
    modulo = math.prod(divisors)
    for r in range(10000):
        for m in monkies:
            make_turn(monkies, 0, modulo, m)
    return monkey_business(monkies)


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 10605)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 2713310158)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        data = f.read()
    print(solve1(parse_input(data)))
    print(solve2(parse_input(data)))
