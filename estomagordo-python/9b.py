from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(lines):
    visited = {(0,0)}
    hy = 0
    hx = 0
    tailsize = 9
    tail = [[0, 0] for _ in range(tailsize)]

    for line in lines:
        move = line.split()
        d = int(move[1])

        for _ in range(d):
            if move[0] == 'L':
                hx -= 1
            elif move[0] == 'R':
                hx += 1
            elif move[0] == 'U':
                hy -= 1
            else:
                hy += 1

            prevy = hy
            prevx = hx

            for i in range(tailsize):
                ty, tx = tail[i]

                if abs(prevy-ty) == 2 or abs(prevx-tx) == 2:
                    dy = 1 if prevy > ty else 0 if prevy == ty else -1
                    dx = 1 if prevx > tx else 0 if prevx == tx else -1

                    ty += dy
                    tx += dx                   

                tail[i] = [ty, tx]
                prevy = ty
                prevx = tx

            visited.add((tail[-1][0], tail[-1][1]))

    
    return len(visited)


def main():
    lines = []

    with open('9.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
