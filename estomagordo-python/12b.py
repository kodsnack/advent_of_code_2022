from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(grid):
    gy = -1
    gx = -1
    seen = set()
    frontier = []

    height = len(grid)
    width = len(grid[0])

    for y in range(height):
        for x in range(width):
            c = grid[y][x]

            if c in 'Sa':
                frontier.append([0, y, x])
                seen.add((y, x))
            if c == 'E':
                gy = y
                gx = x

    for steps, y, x in frontier:
        if y == gy and x == gx:
            return steps

        c = grid[y][x]
        h = ord('a') if c == 'S' else ord(grid[y][x])

        for ny, nx in neighs_bounded(y, x, 0, height-1, 0, width-1):
            if (ny, nx) in seen:
                continue

            nc = grid[ny][nx]
            nh = ord(nc) if nc.islower() else ord('z')

            if nh - h > 1:
                continue

            seen.add((ny, nx))

            frontier.append((steps+1, ny, nx))


def main():
    lines = []

    with open('12.txt') as f:
        for line in f.readlines():
            lines.append(line.rstrip())
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
