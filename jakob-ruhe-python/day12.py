#!/usr/bin/env python3

# Day 12: Hill Climbing Algorithm
# By Jakob Ruhe 2022-12-12

import os
import unittest
from utils import Point, find_neighbors
import heapq


def parse_input(input):
    """Returns a dict of points and their respective height as
    well as the start and the goal.
    """
    rows = input.strip().split("\n")
    heights = {}
    start = None
    goal = None
    for y in range(len(rows)):
        for x in range(len(rows[0])):
            p = Point(x, y)
            c = rows[y][x]
            if c == "S":
                assert start is None
                start = p
                c = "a"
            elif c == "E":
                assert goal is None
                goal = p
                c = "z"
            h = ord(c) - ord("a")
            heights[p] = h
    return heights, start, goal


def can_go(heights, a, b):
    """Returns true if we are able to go from `a` to `b`.
    Note however that we are going down from the top
    to the valley.
    """
    return heights[b] >= heights[a] - 1


def reachable_neighbors(heights, pos):
    """Returns all neighbors we can reach from `pos`"""
    return [n for n in find_neighbors(pos) if n in heights and can_go(heights, pos, n)]


def solve(heights, start, goal):
    """Uses Dijkstra's algorithm to go from `start` to `goal`
    Note that this is called with `start` and `goal` exchanged.
    Returns a dict of distances to `start`.
    Locations that cannot reach `start` are not included in the result.
    """
    distances = {}
    Q = []
    visited = set()

    distances[start] = 0
    heapq.heappush(Q, (0, start))

    while Q:
        dist, current = heapq.heappop(Q)
        if current in visited or current == goal:
            break
        visited.add(current)
        neighbors = reachable_neighbors(heights, current)
        n_dist = distances[current] + 1
        for n in neighbors:
            if n not in distances or distances[n] > n_dist:
                distances[n] = n_dist
                heapq.heappush(Q, (n_dist, n))

    return distances


def solve1(heights, start, goal):
    distances = solve(heights, goal, start)
    return distances[start]


def solve2(heights, start, goal):
    distances = solve(heights, goal, None)
    starts = [k for k, v in heights.items() if v == 0 and k in distances]
    best_start = min(starts, key=lambda s: distances[s])
    return distances[best_start]


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

    def test1(self):
        self.assertEqual(solve1(*parse_input(self.input)), 31)

    def test2(self):
        self.assertEqual(solve2(*parse_input(self.input)), 29)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        heights, start, goal = parse_input(f.read())
    print(solve1(heights, start, goal))
    print(solve2(heights, start, goal))
