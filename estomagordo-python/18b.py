from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, custsort, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(lines):
    droplets = [ints(line) for line in lines]
    ds = {tuple(d) for d in droplets}
    c = 0

    minx = min(d[0] for d in droplets)-1
    miny = min(d[1] for d in droplets)-1
    minz = min(d[2] for d in droplets)-1
    maxx = max(d[0] for d in droplets)+1
    maxy = max(d[1] for d in droplets)+1
    maxz = max(d[2] for d in droplets)+1

    seen = {(minx, miny, minz)}
    frontier = [(minx, miny, minz)]

    def within(t):
        x, y, z = t

        return minx <= x <= maxx and miny <= y <= maxy and minz <= z <= maxz

    for x, y, z in frontier:
        for delta in (-1, 1):
            for coord in range(3):
                neigh = [x, y, z]
                neigh[coord] += delta
                t = tuple(neigh)

                if t in ds:
                    c += 1
                elif t not in seen and within(t):
                    seen.add(t)
                    frontier.append(t)

    return c


def main():
    lines = []

    with open('18.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
