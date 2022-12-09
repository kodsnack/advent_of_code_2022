from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(lines):
    visited = {(0,0)}
    hy = 0
    hx = 0
    ty = 0
    tx = 0

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

            if abs(hy-ty) == 2 or abs(hx-tx) == 2:
                if move[0] == 'L':
                    ty = hy
                    tx = hx + 1
                elif move[0] == 'R':
                    ty = hy
                    tx = hx - 1
                elif move[0] == 'U':
                    ty = hy + 1
                    tx = hx
                else:
                    ty = hy - 1
                    tx = hx

            visited.add((ty, tx))

    return len(visited)



def main():
    lines = []

    with open('9.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
