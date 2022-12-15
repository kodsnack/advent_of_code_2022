from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, custsort, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(lines):
    minx = 0
    maxx = 4000000
    miny = 0
    maxy = 4000000
    beacons = set()
    sensors = []

    for line in lines:
        x, y, bx, by = ints(line)
        beacons.add((bx, by))
        r = abs(x-bx) + abs(y-by)
        sensors.append([x, y, r])

    def iswithin(sx, sy, r, x, y):
        d = abs(sx-x) + abs(sy-y)
        
        return d <= r

    def canhave(minx, maxx, miny, maxy):
        corners = [[minx, miny], [minx, maxy], [maxx, miny], [maxx, maxy]]

        for sx, sy, r in sensors:
            outside = False

            for cx, cy in corners:
                if not iswithin(sx, sy, r, cx, cy):
                    outside = True
                    break

            if not outside:
                return False

        return True
    
    frontier = [[(maxx-miny+1) * (maxy-miny+1), minx, maxx, miny, maxy]]

    while True:
        size, minx, maxx, miny, maxy = heappop(frontier)

        if size == 1:
            return 4000000 * minx + miny

        midx = (minx+maxx)//2
        midy = (miny+maxy)//2

        rects = [
            [minx, midx, miny, midy],
            [minx, midx, midy, maxy],
            [midx, maxx, miny, midy],
            [midx, maxx, midy, maxy]
        ]

        if size == 4:
            rects = [
                [minx, minx, miny, miny],
                [minx, minx, maxy, maxy],
                [maxx, maxx, miny, miny],
                [maxx, maxx, maxy, maxy]
            ]

        for rminx, rmaxx, rminy, rmaxy in rects:
            if canhave(rminx, rmaxx, rminy, rmaxy):
                area = (rmaxx-rminx+1) * (rmaxy-rminy+1)
                heappush(frontier, (area, rminx, rmaxx, rminy, rmaxy))


def main():
    lines = []

    with open('15.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
