from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(grid):
    height = len(grid)
    width = len(grid[0])

    count = 0

    for y in range(height):
        for x in range(width):
            h = grid[y][x]

            if any(ray == [] or all(tree < h for tree in ray) for ray in rays(grid, y, x)):
                count += 1

    return count


def main():
    lines = []

    with open('8.txt') as f:
        for line in f.readlines():
            lines.append(digits(line))
            
    return solve(lines)


if __name__ == '__main__':
    print(main())