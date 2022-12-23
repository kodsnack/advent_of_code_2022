from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, custsort, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(lines):
    rocks = set()
    sand = set()

    for line in lines:
        nums = ints(line)
        n = len(nums)

        x, y = nums[0], nums[1]
        rocks.add((x, y))

        for dx in range(2, n, 2):
            nx, ny = nums[dx], nums[dx+1]

            if nx > x:
                for hx in range(x, nx+1):
                    rocks.add((hx, y))
            if nx < x:
                for hx in range(nx, x+1):
                    rocks.add((hx, y))
            if ny > y:
                for hy in range(y, ny+1):
                    rocks.add((x, hy))
            if ny < y:
                for hy in range(ny, y+1):
                    rocks.add((x, hy))

            x, y = nx, ny

    bottommost = max(r[1] for r in rocks)
    
    while True:
        sx, sy = 500, 0
        keepgoing = True

        while keepgoing:
            keepgoing = False
            while sy < bottommost+1:
                if (sx, sy+1) not in rocks and (sx, sy+1) not in sand:
                    sy += 1
                    keepgoing = True
                    continue
                if (sx-1, sy+1) not in rocks and (sx-1, sy+1) not in sand:
                    sy += 1
                    sx -= 1
                    keepgoing = True
                    continue
                if (sx+1, sy+1) not in rocks and (sx+1, sy+1) not in sand:
                    sy += 1
                    sx += 1
                    keepgoing = True
                    continue
                break

        if (sx, sy) in sand:
            break

        sand.add((sx, sy))

    return len(sand)


def main():
    lines = []

    with open('14.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())