from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import adjacent, chunks, chunks_with_overlap, columns, custsort, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(lines):
    grid = [line.rstrip() for line in lines]
    h = len(grid)
    w = len(grid[0])
    sy = 0
    sx = -1
    gy = h-1
    gx = -1

    blizzards = []
    unmovable = set()

    for y in range(h):
        for x in range(w):
            c = grid[y][x]

            if sx == -1 and c == '.':
                sx = x

            if y == h-1 and c == '.':
                gx = x

            if c == '>':
                blizzards.append([y, x, 0, 1])
                unmovable.add((0, y, x))
            if c == '<':
                blizzards.append([y, x, 0, -1])
                unmovable.add((0, y, x))
            if c == '^':
                blizzards.append([y, x, -1, 0])
                unmovable.add((0, y, x))
            if c == 'v':
                blizzards.append([y, x, 1, 0])
                unmovable.add((0, y, x))


    blizzlim = 1000

    for t in range(1, blizzlim):
        newblizz = []

        for y, x, dy, dx in blizzards:
            ny = y+dy
            nx = x + dx

            if ny == 0:
                ny = h-2
            if ny == h-1:
                ny = 1
            if nx == 0:
                nx = w-2
            if nx == w-1:
                nx = 1

            newblizz.append([ny, nx, dy, dx])

        blizzards = newblizz

        for by, bx, _, _ in blizzards:
            unmovable.add((t, by, bx))

    frontier = [[0, sy, sx]]
    seen = {(0, sy, sx)}

    while True:
        t, y, x = heappop(frontier)

        if y == gy and x == gx:
            return t

        if not (t+1, y, x) in unmovable:
            seen.add((t+1, y, x))
            heappush(frontier, [t+1, y, x])

        for ny, nx in neighs(y, x):
            if grid[ny][nx] == '#':
                continue

            if (t+1, ny, nx) in unmovable:
                continue

            if (t+1, ny, nx) in seen:
                continue

            seen.add((t+1, ny, nx))

            heappush(frontier, [t+1, ny, nx])



def main():
    lines = []

    with open('24.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
