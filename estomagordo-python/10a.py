from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(lines):
    intervals = [20, 60, 100, 140, 180, 220]
    total = 0
    x = 1
    cycle = 1

    for line in lines:
        if cycle in intervals:
            total += cycle * x

        if line.rstrip() == 'noop':
            cycle += 1
        else:
            val = int(line.split()[1])

            if cycle+1 in intervals:
                total += (cycle+1) * x

            cycle += 2
            x += val

    if cycle in intervals:
        total += cycle * x

    return total


def main():
    lines = []

    with open('10.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
