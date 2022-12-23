from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import adjacent, chunks, chunks_with_overlap, columns, custsort, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(lines):
    elves = set()

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                elves.add((y, x))

    turnorder = [
        [[-1, 0], [-1, -1], [-1, 1]],
        [[1, 0], [1, -1], [1, 1]],
        [[0, -1], [-1, -1], [1, -1]],
        [[0, 1], [-1, 1], [1, 1]]
    ]

    round = 1

    while True:
        roundmoves = defaultdict(list)

        for y, x in elves:            
            if not any((ny, nx) in elves for ny, nx in eight_neighs(y, x)):
                continue
            
            for dmove in range(4):
                move = turnorder[(round-1+dmove)%4]

                if not any((y+my, x+mx) in elves for my, mx in move):
                    roundmoves[(y+move[0][0], x+move[0][1])].append((y, x))
                    break

        moved = False
        
        for my, mx in roundmoves.keys():
            if len(roundmoves[(my, mx)]) > 1:
                continue

            oy, ox = roundmoves[(my, mx)][0]
            moved = True
            elves.add((my, mx))
            elves.remove((oy, ox))

        if not moved:
            return round

        round += 1


def main():
    lines = []

    with open('23.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
