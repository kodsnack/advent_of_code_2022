from collections import Counter, defaultdict, deque
from functools import reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import adjacent, chunks, chunks_with_overlap, columns, custsort, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside
from time import time as ti
from sys import getsizeof

def solve(lines):
    blueprints = [ints(line) for line in lines]

    # blueprints = [[1, 4, 2, 3, 14, 2, 7], [2, 2, 3, 3, 8, 3, 12]]

    def score(blueprint, time=24):
        state = (time, 0, 0, 0, 0, 1, 0, 0, 0)
        frontier = [state]
        seen = {}
        best = 0
        # latest = time
        # tt = ti()

        for t, ore, clay, obs, geo, orebot, claybot, obsbot, geobot in frontier:
            # if t < latest:
            #     latest = t
            #     print(latest, len(frontier), len(seen), ti()-tt)
            #     tt = ti()

            if t == 0:
                best = max(best, geo)
                continue

            moves = [[t-1, ore+orebot, clay+claybot, obs+obsbot, geo+geobot, orebot, claybot, obsbot, geobot]]

            if ore >= blueprint[4] and obs >= blueprint[5]:
                moves.append([t-1, ore+orebot-blueprint[4], clay+claybot, obs+obsbot-blueprint[5], geo+geobot, orebot, claybot, obsbot, geobot+1])
            else:
                if ore >= blueprint[2] and clay >= blueprint[3]:
                    moves.append([t-1, ore+orebot-blueprint[2], clay+claybot-blueprint[3], obs+obsbot, geo+geobot, orebot, claybot, obsbot+1, geobot])
                if ore >= blueprint[1] and t > 2:
                    moves.append([t-1, ore+orebot-blueprint[1], clay+claybot, obs+obsbot, geo+geobot, orebot, claybot+1, obsbot, geobot])
                if ore >= blueprint[0] and t > 1:
                    moves.append([t-1, ore+orebot-blueprint[0], clay+claybot, obs+obsbot, geo+geobot, orebot+1, claybot, obsbot, geobot])
                    
            for move in moves:
                tup = tuple(move[2:])

                if tup in seen and seen[tup] >= move[1]:
                    continue

                seen[tup] = move[1]
                frontier.append(move)

        return best

    s = 0

    for b in blueprints:
        tt = ti()
        sc = score(b[1:])
        s += b[0] * sc
        print(b[0], sc, s, ti()-tt)
        tt = ti()

    return s


def main():
    lines = []

    with open('19.txt') as f:
        for line in f.readlines():
            lines.append(line)

    return solve(lines)


if __name__ == '__main__':
    print(main())

# 2181 too high
# 787 too low
