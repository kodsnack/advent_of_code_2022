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

    leftmost = min(r[0] for r in rocks)
    rightmost = max(r[0] for r in rocks)
    bottommost = max(r[1] for r in rocks)
    
    while True:
        print(len(sand))
        sx, sy = 500, 0
        keepgoing = True

        while keepgoing:
            while sx >= leftmost and sx <= rightmost and sy < bottommost:
                if (sx, sy+1) not in rocks and (sx, sy+1) not in sand:
                    sy += 1
                    continue
                if (sx-1, sy+1) not in rocks and (sx-1, sy+1) not in sand:
                    sy += 1
                    sx -= 1
                    continue
                if (sx+1, sy+1) not in rocks and (sx+1, sy+1) not in sand:
                    sy += 1
                    sx += 1
                    continue
                keepgoing = False
                break

            # if sx < leftmost or sx > rightmost or sy > bottommost:
            #     break

            # keepgoing = False
            # # fell = False

            # while (sx, sy+1) not in rocks and (sx, sy+1) not in sand and sy+1 < bottommost:
            #     # fell = True
            #     sy += 1

            # # if fell:
            # #     continue

            # if (sx-1, sy+1) not in rocks and (sx-1, sy+1) not in sand:
            #     sx -= 1
            #     sy += 1
            #     keepgoing = True
            # elif (sx+1, sy+1) not in rocks and (sx+1, sy+1) not in sand:
            #     sx += 1
            #     sy += 1
            #     keepgoing = True

        if sx < leftmost or sx > rightmost:
            break

        if (sx, sy) in sand:
            break

        sand.add((sx, sy))

    for y in range(0, bottommost+1):
        row = ''

        for x in range(leftmost, rightmost+1):
            if (x, y) in rocks:
                row += '#'
            elif (x, y) in sand:
                row += 'O'
            elif x == 500 and y == 0:
                row += '+'
            else:
                row += '.'

        print(row)
    
    return len(sand)


def main():
    lines = []

    with open('14.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())


# 873
# 1395
# 1376