from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, custsort, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(lines):
    moves = lines[0].rstrip()
    m = len(moves)
    shapes = [
        [(0, 2), (0, 3), (0, 4), (0, 5)],
        [(0, 3), (1, 2), (1, 3), (1, 4), (2, 3)],
        [(0, 2), (0, 3), (0, 4), (1, 4), (2, 4)],
        [(0, 2), (1, 2), (2, 2), (3, 2)],
        [(0, 2), (0, 3), (1, 2), (1, 3)]
    ]

    def step(solid, shapenum, movepos, bottom):
        shape = [[bottom+4+s[0], s[1]] for s in shapes[shapenum%5]]

        while True:
            push = 1 if moves[movepos%m] == '>' else -1
            cango = True

            for y, x in shape:
                if not -1 < x + push < 7:
                    cango = False
                    break

                if (y, x+push) in solid:
                    cango = False
                    break

            if cango:
                for i in range(len(shape)):
                    shape[i][1] += push

            movepos += 1

            canfall = True

            for y, x in shape:
                if (y-1, x) in solid:
                    canfall = False
                    break

            if not canfall:
                break

            for i in range(len(shape)):
                shape[i][0] -= 1
        
        for y, x in shape:
            solid.add((y, x))
            bottom = max(bottom, y)

        return solid, movepos, bottom
            
    n = len(shapes)
    solid = {(0, x) for x in range(7)}
    bottom = 0
    shapenum = 0
    movepos = 0    
    cycledetectlen = 25000
    cyclegrowths = Counter()
    steps = 0

    for _ in range(cycledetectlen):
        solid, movepos, bottom = step(solid, shapenum, movepos, bottom)
        steps += 1
        shapenum += 1

        if shapenum % n == 0:
            cyclegrowths[movepos%m] += 1

    cyclen = n * len([k for k in cyclegrowths.keys() if cyclegrowths[k] > 1])
    target = 1000000000000
    cycstart = bottom

    for _ in range(cyclen):
        solid, movepos, bottom = step(solid, shapenum, movepos, bottom)
        steps += 1
        shapenum += 1
        
    cycval = bottom-cycstart

    while (target-steps)%cyclen:
        solid, movepos, bottom = step(solid, shapenum, movepos, bottom)
        steps += 1

    return bottom + (target-steps)//cyclen * cycval


def main():
    lines = []

    with open('17.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())