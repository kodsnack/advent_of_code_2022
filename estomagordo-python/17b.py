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
            
    solid = {(0, x) for x in range(7)}
    bottom = 0
    shapenum = 0
    movepos = 0    
    cycledetectlen = 25000
    cyclegrowths = Counter()
    lastcycle = 0

    for _ in range(cycledetectlen):
        solid, movepos, bottom = step(solid, shapenum, movepos, bottom)
        shapenum += 1

        if shapenum % 5 == 0:
            cyclegrowths[bottom-lastcycle] += 1
            lastcycle = bottom

    cyclen = 345*5
    prev = n-cyclen
    prevbot = 0
    target = 1000000000000
    magic = 579710000
    bottom = 0    
    last = 0
    
    
    cycval = bottom-prevbot

    return bottom + cycval * magic


def main():
    lines = []

    with open('17.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())