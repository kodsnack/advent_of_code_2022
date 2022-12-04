from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives


def solve(lines):
    def rangify(line):
        a, b, c, d = positives(line)
        return {num for num in range(a, b+1)}, {num for num in range(c, d+1)}

    def overlaps(a, b):
        return len(a&b) > 0

    return sum(overlaps(*rangify(line)) for line in lines)


def main():
    lines = []

    with open('4.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
