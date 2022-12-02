from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded


def solve(lines):
    score = 0

    for a, b in lines:
        x = ord(a) - ord('A')

        score += 3 * (ord(b) - ord('X'))

        if b == 'X':
            score += (x-1)%3 + 1
        if b == 'Y':
            score += x + 1
        if b == 'Z':
            score += (x+1)%3 + 1

    return score


def main():
    lines = []

    with open('2.txt') as f:
        for line in f.readlines():
            lines.append(line.split())
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
