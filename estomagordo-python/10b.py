from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(lines):
    image = [['.' for _ in range(40)] for _ in range(6)]
    x = 1
    cycle = 1

    for line in lines:
        drawpos = (cycle-1) % 40 + 1
        row = (cycle-1)//40

        if drawpos in (x-1, x, x):
            image[row][drawpos-1] = '#'

        if line.rstrip() == 'noop':
            cycle += 1
        else:
            val = int(line.split()[1])

            cycle += 1
            drawpos = (cycle-1) % 40 + 1
            row = (cycle-1)//40

            if drawpos in (x-1, x, x):
                image[row][drawpos-1] = '#'

            cycle += 1
            x += val

    for line in image:
        print(''.join(line))


def main():
    lines = []

    with open('10.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
