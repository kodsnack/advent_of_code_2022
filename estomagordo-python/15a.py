from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, custsort, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(lines):
    keyline = 2000000
    nots = set()

    for line in lines:
        x, y, bx, by = ints(line)
        d = abs(bx-x) + abs(by-y)

        for dx in range(-d, d+1):           
            nd = abs(dx) + abs(keyline-y)
            if nd <= d and (x+dx, keyline) and (dx != 0 or keyline != y) and (x+dx != bx or by != keyline):
                nots.add(x+dx)

    return len(nots)


def main():
    lines = []

    with open('15.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
