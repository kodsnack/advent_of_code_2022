from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, custsort, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(lines):
    droplets = [ints(line) for line in lines]

    c = 0

    for d in droplets:
        x, y, z = d
        c += 6
        
        for delta in (-1, 1):
            for coord in range(3):
                neigh = list(d)
                neigh[coord] += delta

                if neigh in droplets:
                    c -= 1

    return c


def main():
    lines = []

    with open('18.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
