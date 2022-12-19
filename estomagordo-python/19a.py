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
        def triang(n):
            if n < 1:
                return 0

            return (n + n*n)//2

        def heuristic(state):
            time = state[0]
            geo = state[4]
            geobot = state[8]

            return geo + geobot * time + triang(time-1)

        def encode(state):
            val = 0
            base = 1

            for x in state[2:]:
                val += base * x
                base *= 1000

            return (state[0], state[1], val)

        def decode(encoded):
            state = [encoded[0], encoded[1]]
            val = encoded[2]

            for _ in range(8):
                state.append(val%1000)
                val //= 1000

            return state

        state = (time, 0, 0, 0, 0, 1, 0, 0, 0)
        # seen = {(0, 1, 0, 0, 0)}
        starth = heuristic(state)
        state = tuple([-starth] + list(state))
        frontier = [encode(state)]
        taken = 0
        latest = time
        best = 0
        tt = ti()

        while frontier:
            taken += 1
            negh, t, ore, clay, obs, geo, orebot, claybot, obsbot, geobot = decode(heappop(frontier))
            latest = min(latest, t)

            if taken % 10**7 == 0:
                print(taken, len(frontier), getsizeof(frontier), latest, -negh, ti()-tt)
                tt = ti()

            # if t < latest:
            #     print(t)
            #     latest = t

            if t == 0:
                print(taken, len(frontier))
                return geo

            moves = [[t-1, ore+orebot, clay+claybot, obs+obsbot, geo+geobot, orebot, claybot, obsbot, geobot]]

            if ore >= blueprint[4] and obs >= blueprint[5] and t > 2:
                moves = [[t-1, ore+orebot-blueprint[4], clay+claybot, obs+obsbot-blueprint[5], geo+geobot, orebot, claybot, obsbot, geobot+1]]
                # moves.append([t-1, ore+orebot-blueprint[4], clay+claybot, obs+obsbot-blueprint[5], geo+geobot, orebot, claybot, obsbot, geobot+1])
            elif ore >= blueprint[2] and clay >= blueprint[3] and t > 3:
                # moves = [[t-1, ore+orebot-blueprint[2], clay+claybot-blueprint[3], obs+obsbot, geo+geobot, orebot, claybot, obsbot+1, geobot]]
                moves.append([t-1, ore+orebot-blueprint[2], clay+claybot-blueprint[3], obs+obsbot, geo+geobot, orebot, claybot, obsbot+1, geobot])
            else:
                if ore >= blueprint[1] and t > 2:
                    moves.append([t-1, ore+orebot-blueprint[1], clay+claybot, obs+obsbot, geo+geobot, orebot, claybot+1, obsbot, geobot])
                if ore >= blueprint[0] and t > 1:
                    moves.append([t-1, ore+orebot-blueprint[0], clay+claybot, obs+obsbot, geo+geobot, orebot+1, claybot, obsbot, geobot])

            if len(moves) == 5:
                moves = moves[1:]

            for move in moves:
                # tup = (move[0], move[5], move[6], move[7], move[8])

                # if tup in seen:
                #     continue

                # move[1] += move[5]
                # move[2] += move[6]
                # move[3] += move[7]
                # move[4] += move[8]

                # seen.add(t)

                # print(len(seen), taken)

                h = heuristic(move)

                mstate = tuple([-h] + move)

                heappush(frontier, encode(mstate))

        return best

    s = 0

    for b in blueprints:
        tt = ti()
        sc = score(b[1:])
        print(b[0], sc, ti()-tt)
        tt = ti()
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
