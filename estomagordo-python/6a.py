from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives


def solve(signal):
    length = 4
    x = length

    while len(set(signal[x-length:x])) < length:
        x += 1

    return x


def main():
    with open('6.txt') as f:
        for line in f.readlines():
            return solve(line)


if __name__ == '__main__':
    print(main())
