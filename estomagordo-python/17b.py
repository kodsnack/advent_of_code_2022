from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, custsort, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(lines):
    moves = lines[0].rstrip()
    m = len(moves)
    p = 0
    shapes = [
        [(0, 2), (0, 3), (0, 4), (0, 5)],
        [(0, 3), (1, 2), (1, 3), (1, 4), (2, 3)],
        [(0, 2), (0, 3), (0, 4), (1, 4), (2, 4)],
        [(0, 2), (1, 2), (2, 2), (3, 2)],
        [(0, 2), (0, 3), (1, 2), (1, 3)]
    ]

    solid = {(0, x) for x in range(7)}
    n = 2500
    cyclen = 35
    prev = n-cyclen
    prevbot = 0
    target = 1000000000000
    magic = 28571428500
    c = Counter()
    bottom = 0
    
    last = 0
    
    for x in range(n):
        if x == prev:
            prevbot = bottom
        if x > 0 and x % 5 == 0:
            if x > 500:
                c[(p%m, bottom-last)] += 1
            last = bottom
        # if x > 0 and x % 5 == 0 and p % m == 0:
        #     print(x)
        #     c[(lastholes, bottom-last)] += 1
        #     last = bottom
        #     lastholes = holes()

        shape = []

        for y, x in shapes[x%5]:
            shape.append([bottom+4+y, x])

        while True:
            push = 1 if moves[p % m] == '>' else -1
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

            p += 1

            canfall = True

            for y, x in shape:
                if (y-1, x) in solid:
                    canfall = False
                    break

            if not canfall:
                break

            for i in range(len(shape)):
                shape[i][0] -= 1
        a=2
        for y, x in shape:
            solid.add((y, x))
            bottom = max(bottom, y)

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
