from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, custsort, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(lines):
    valves = {}

    for line in lines:
        parts = line.split()
        name = parts[1]
        val = ints(line)[0]

        nexts = parts[9:]
        l = []

        for ne in nexts:
            if ne[-1] == ',':
                l.append(ne[:-1])
            else:
                l.append(ne)

        valves[name] = [val, l]

    useful = [k for k in valves.keys() if valves[k][0] > 0]
    distances = {}

    for u in useful + ['AA']:
        seen = {u}
        frontier = [(0, u)]
        mapping = {}

        for steps, valve in frontier:
            if valve in useful:
                mapping[valve] = steps

            for neigh in valves[valve][1]:
                if neigh in seen:
                    continue

                seen.add(neigh)

                frontier.append((steps+1, neigh))

        distances[u] = mapping

    def optimize(limit, start, usable):
        frontier = [[limit, 0, start, []]]
        paths = set()
        highest = 0
        best = []

        while frontier:
            remaining, score, valve, used = heappop(frontier)

            if score > highest:
                highest = score
                best = used

            if remaining == 0:
                continue

            if valve in usable and valve not in used:
                heappush(frontier, [remaining-1, score + valves[valve][0] * (remaining-1), valve, used + [valve]])

            for u in usable:
                if u in used:
                    continue

                if u == valve:
                    continue

                taking = distances[valve][u]
                arrival = remaining-taking

                if arrival > 0:
                    t = tuple(used + [u])

                    if t not in paths:
                        paths.add(t)
                        heappush(frontier, [arrival, score, u, list(used)])

        return highest, best
    
    return optimize(30, 'AA', useful)[0]


def main():
    lines = []

    with open('16.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
