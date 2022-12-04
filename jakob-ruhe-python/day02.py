#!/usr/bin/env python3

# By Jakob Ruhe 2022-12-02

import os
import unittest


def parse_input(input):
    return input.strip().split("\n")


def hand_as_num(hand, rock):
    return ord(hand) - ord(rock)


def winning_hand(h):
    return (h + 1) % 3


def loosing_hand(h):
    return (h - 1) % 3


def game_result(opp_hand, my_hand):
    wh = winning_hand(opp_hand)
    return "Z" if my_hand == wh else ("Y" if my_hand == opp_hand else "X")


def hand_points(h):
    return h + 1


def game_points(result):
    scores = {"X": 0, "Y": 3, "Z": 6}
    return scores[result]


def solve1(entries):
    # The first column is what your opponent is going to play:
    # A for Rock, B for Paper, and C for Scissors.
    total = 0
    for e in entries:
        h1, h2 = e.split(" ")
        opp_hand = hand_as_num(h1, "A")
        my_hand = hand_as_num(h2, "X")
        result = game_result(opp_hand, my_hand)
        total += hand_points(my_hand) + game_points(result)
    return total


def solve2(entries):
    # X means you need to lose, Y means you need to end the round in a draw,
    # and Z means you need to win.
    total = 0
    for e in entries:
        h1, result = e.split(" ")
        opp_hand = hand_as_num(h1, "A")
        my_hand = (
            winning_hand(opp_hand)
            if result == "Z"
            else loosing_hand(opp_hand)
            if result == "X"
            else opp_hand
        )
        calculated_result = game_result(opp_hand, my_hand)
        assert calculated_result == result
        total += hand_points(my_hand) + game_points(result)
    return total


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
A Y
B X
C Z
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 15)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 12)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
