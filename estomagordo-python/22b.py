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

    for yy in range(height):
        diff = width - len(grid[yy])
        grid[yy] += ' ' * diff

    def cubeface(y, x):
        if y < 0:
            print('above all')
        if y > 199:
            print('below all')
        if x < 0:
            print('left all?')
        if x > 149:
            print('right all!')
        if y < 50:
            if x < 100:
                if x < 50:
                    print('to the left of 1')
                return 1
            if x > 149:
                print('to the right of 2')
            return 2
        if y < 100:
            if x < 50:
                print('to the left of 3')
            if x > 99:
                print('to the right of 3')
            return 3
        if y < 150:
            if x < 50:
                return 4
            if x > 99:
                print('to the right of 5')
            return 5
        if y > 199:
            print('too far down')
        if x > 49:
            print('to the right of 6')
        return 6

    cubelims = [
        [-1, -1, -1, -1],
        [0, 49, 50, 99],
        [0, 49, 100, 149],
        [50, 99, 50, 99],
        [100, 149, 0, 49],
        [100, 149, 50, 99],
        [150, 199, 0, 49]
    ]

    @cache
    def nextfrom(y, x, direction):
        dy, dx = directions[direction%4]
        cube = cubeface(y, x)
        miny, maxy, minx, maxx = cubelims[cube]

        ny = y + dy
        nx = x + dx

        if ny < miny:
            if cube == 1:
                ny = x + 100
                nx = 0
                direction = 0
            if cube == 2:
                ny = 199
                nx = x - 100
                direction = 3
            if cube == 3:
                ny = y - 1
                nx = x
                direction = 3
            if cube == 4:
                ny = x + 50
                nx = 50
                direction = 0
            if cube == 5:
                ny = y - 1
                nx = x
                direction = 3
            if cube == 6:
                ny = y - 1
                nx = x
                direction = 3
        elif ny > maxy:
            if cube == 1:
                ny = y + 1
                nx = x
                direction = 1
            if cube == 2:
                ny = x - 50
                nx = 99
                direction = 2
            if cube == 3:
                ny = y + 1
                nx = x
                direction = 1
            if cube == 4:
                ny = y + 1
                nx = x
                direction = 1
            if cube == 5:
                ny = x + 100
                nx = 49
                direction = 2
            if cube == 6:
                ny = 0
                nx = x + 100
                direction = 1
        elif nx < minx:
            if cube == 1:
                ny = 149 - y
                nx = 0
                direction = 0
            if cube == 2:
                ny = y
                nx = x - 1
                direction = 2
            if cube == 3:
                ny = 100
                nx = y - 50
                direction = 1
            if cube == 4:
                ny = 149 - y
                nx = 50
                direction = 0
            if cube == 5:
                ny = y
                nx = x - 1
                direction = 2
            if cube == 6:
                ny = 0
                nx = y - 100
                direction = 1
        elif nx > maxx:
            if cube == 1:
                ny = y
                nx = x + 1
                direction = 0
            if cube == 2:
                ny = x
                nx = 99
                direction = 2
            if cube == 3:
                ny = 49
                nx = y + 50
                direction = 3
            if cube == 4:
                ny = y
                nx = x + 1
                direction = 0
            if cube == 5:
                ny = 149 - y
                nx = 149
                direction = 2
            if cube == 6:
                ny = 149
                nx = y - 100
                direction = 3
    
        return (ny, nx, direction)
        # print(y, x, ny, nx, origdir, cubeface(y, x))

    for xx in range(width):
        if grid[0][xx] == '.':
            x = xx
            break

    while command < len(steps):
        taking = steps[command]
        taken = 0

        while taken < taking:
            ny, nx, nfacing = nextfrom(y, x, facing)

            if grid[ny][nx] == '#':
                break

            y = ny
            x = nx
            facing = nfacing

            taken += 1

        if taken == 0:
            dy, dx = directions[facing%4]
            ny = y + dy
            nx = x + dx

            if (grid[ny][nx]) == '.':
                print(command, taking, facing)

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

# 149643 too high
# 154139
# 49474 too high