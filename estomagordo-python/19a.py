from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import adjacent, chunks, chunks_with_overlap, columns, custsort, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(lines):
    blueprints = [ints(line) for line in lines]

    # blueprints = [[1, 4, 2, 3, 14, 2, 7], [2, 2, 3, 3, 8, 3, 12]]

    def score(blueprint, time=24):
        def triang(n):
            if n < 1:
                return 0

            return (n + n*n)//2

        def heuristic(state):
            time = state[0]
            geo = state[4]
            geobot = state[8]

            return geo + geobot * time + triang(time-2)

        state = (time, 0, 0, 0, 0, 1, 0, 0, 0)
        seen = {(0, 1, 0, 0, 0)}
        starth = heuristic(state)
        state = tuple([-starth] + list(state))
        frontier = [state]
        taken = 0
        # latest = time
        best = 0

        while frontier:
            taken += 1
            _, t, ore, clay, obs, geo, orebot, claybot, obsbot, geobot = heappop(frontier)

            # if t < latest:
            #     print(t)
            #     latest = t

            if t == 0:
                return geo

            moves = [[t-1, ore+orebot, clay+claybot, obs+obsbot, geo+geobot, orebot, claybot, obsbot, geobot]]
            
            if ore >= blueprint[4] and obs >= blueprint[5]:
                moves.append([t-1, ore+orebot-blueprint[4], clay+claybot, obs+obsbot-blueprint[5], geo+geobot, orebot, claybot, obsbot, geobot+1])
            if ore >= blueprint[2] and clay >= blueprint[3]:
                moves.append([t-1, ore+orebot-blueprint[2], clay+claybot-blueprint[3], obs+obsbot, geo+geobot, orebot, claybot, obsbot+1, geobot])
            if ore >= blueprint[1]:
                moves.append([t-1, ore+orebot-blueprint[1], clay+claybot, obs+obsbot, geo+geobot, orebot, claybot+1, obsbot, geobot])
            if ore >= blueprint[0]:
                moves.append([t-1, ore+orebot-blueprint[0], clay+claybot, obs+obsbot, geo+geobot, orebot+1, claybot, obsbot, geobot])

            for move in moves:
                tup = (move[0], move[5], move[6], move[7], move[8])

                if tup in seen:
                    continue

                # move[1] += move[5]
                # move[2] += move[6]
                # move[3] += move[7]
                # move[4] += move[8]

                seen.add(t)

                # print(len(seen), taken)

                h = heuristic(move)

                mstate = tuple([-h] + move)

                heappush(frontier, mstate)

        return best

    s = 0

    for b in blueprints:
        sc = score(b[1:])
        print(b[0], sc)
        s += b[0] * sc

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