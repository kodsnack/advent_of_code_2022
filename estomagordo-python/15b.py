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

    def iswithin(sensor, x, y):
        sx, sy, r = sensor
        d = abs(sx-x) + abs(sy-y)
        
        return d <= r

    
    
    while minx < maxx and miny < maxy:
        sx = (minx+maxx)//2
        sy = (miny+maxy)//2

        print(sx, sy)

        if not any(iswithin(sensor, sx, sy) for sensor in sensors):
            return sx * 4000000 + sy

        goup = False
        godown = False
        goleft = False
        goright = False

        for sensor in sensors:
            if not iswithin(sensor, sx, sy):
                continue

            xdiff = abs(sx-sensor[0])
            ydiff = abs(sy-sensor[1])

            if xdiff <= ydiff:
                if sx > sensor[0]:
                    goright = True
                else:
                    goleft = True
            elif sy > sensor[1]:
                godown = True
            else:
                goup = True

        if goup:
            miny = sy+1
        else:
            maxy = sy-1
        if goright:
            minx = sx+1
        else:
            maxx = sx-1


def main():
    lines = []

    with open('15.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
