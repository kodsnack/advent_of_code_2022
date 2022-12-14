from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded


def solve(games):
    score = 0

    def outcome(a, b):
        x = ord(a) - ord('A')
        y = ord(b) - ord('X')

        if x == y:
            return 3

        if (y-1) % 3 == x:
            return 6

        return 0

    for a, b in games:
        score += ord(b) - ord('X') + 1
        score += outcome(a, b)

    return score


def main():
    lines = []

    with open('2.txt') as f:
        for line in f.readlines():
            lines.append(line.split())
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
