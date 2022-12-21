#!/usr/bin/env python3

# Day 20: Grove Positioning System
# By Jakob Ruhe 2022-12-20

import os
import unittest


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


def parse_input(input):
    return [int(line) for line in input.strip().split("\n")]


def node_pop(node):
    prev = node.prev
    node.prev.next = node.next
    node.next.prev = node.prev
    node.next = node.prev = None
    return prev


def node_push_after(position, node):
    assert node.prev is None and node.next is None
    assert position.prev is not None and position.next is not None
    node.prev = position
    node.next = position.next
    node.next.prev = position.next = node


def next_n(node, steps):
    for _ in range(steps):
        node = node.next
    return node


def prev_n(node, steps):
    for _ in range(steps):
        node = node.prev
    return node


def find_node(first, value):
    node = first
    while node.data != value:
        node = node.next
        if node == first:
            return None
    return node


def solve(numbers, key, num_times_to_mix):
    N = len(numbers)
    nodes = [Node(n * key) for n in numbers]
    for i, node in enumerate(nodes):
        node.next = nodes[(i + 1) % N]
        node.prev = nodes[(i - 1) % N]
    for _ in range(num_times_to_mix):
        for node in nodes:
            step_func = prev_n if node.data < 0 else next_n
            steps = abs(node.data) % (N - 1)
            pos = node_pop(node)
            new_pos = step_func(pos, steps)
            node_push_after(new_pos, node)
    zero = find_node(nodes[0], 0)
    return sum([next_n(zero, (i * 1000) % N).data for i in range(1, 4)])


def solve1(numbers):
    return solve(numbers, 1, 1)


def solve2(numbers):
    return solve(numbers, 811589153, 10)


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
1
2
-3
3
-2
0
4
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 3)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 1623178306)
        pass


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
