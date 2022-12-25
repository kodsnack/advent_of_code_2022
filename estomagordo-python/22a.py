from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import adjacent, chunks, chunks_with_overlap, columns, custsort, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(lines):
    cells, instructions = grouped_lines(lines)
    grid = [line[:-1] if line[-1] == '\n' else line for line in cells]
    steps = ints(instructions[0])
    turns = []

    for c in instructions[0]:
        if c == 'R':
            turns.append(1)
        if c == 'L':
            turns.append(-1)

    directions = [
        [0, 1],
        [1, 0],
        [0, -1],
        [-1, 0]
    ]

    height = len(grid)
    width = max(len(grid[y]) for y in range(height))
    y = 0
    x = -1
    facing = 0
    command = 0

    for y in range(height):
        diff = width - len(grid[y])
        grid[y] += ' ' * diff

    @cache
    def nextfrom(y, x, direction):
        dy = directions[direction%4][0]
        dx = directions[direction%4][1]

        ny = y + dy
        nx = x + dx

        if ny < 0:
            ny = height-1
        if ny == height:
            ny = 0
        if nx < 0:
            nx = len(grid[ny])-1
        if nx >= len(grid[ny]):
            nx = 0

        while grid[ny][nx] == ' ':
            ny += dy
            nx += dx

            if ny < 0:
                ny = height-1
            if ny == height:
                ny = 0
            if nx < 0:
                nx = len(grid[ny])-1
            if nx >= len(grid[ny]):
                nx = 0

        if grid[ny][nx] == '#':
            return (y, x)
        return (ny, nx)

    for xx in range(width):
        if grid[0][xx] == '.':
            x = xx
            break

    while command < len(steps):
        taking = steps[command]
        taken = 0

        while taken < taking:
            ny, nx = nextfrom(y, x, facing)

            if ny == y and nx == x:
                break

            y = ny
            x = nx

            taken += 1

        if command < len(turns):
            facing += turns[command]

        command += 1

    return 1000 * (y+1) + 4 * (x+1) + facing % 4


def main():
    lines = []

    with open('22.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())