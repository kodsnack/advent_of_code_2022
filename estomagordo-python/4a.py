from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded


def solve(lines):
    count = 0

    for l in lines:
        a, b = l.split(',')

        c,d = map(int, a.split('-'))
        e,f = map(int, b.split('-'))

        if (c >= e and d <= f) or (e >= c and f <= d):
            count += 1

    return count


def main():
    lines = []

    with open('4.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
