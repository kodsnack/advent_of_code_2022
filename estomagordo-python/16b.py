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

    # opened = set()
    limit = 26
    # best = 0
    frontier = [[limit, 0, 'AA', 'AA', []]]
    # seen = defaultdict(set)
    paths = set()
    highest = 0

    while frontier:
        remaining, score, me, elephant, used = heappop(frontier)

        if score > highest:
            print(score, used, limit-remaining)
            highest = score

        if remaining == 0:
            continue

        # if remaining == 0:
        #     best = max(best, released)
        #     continue

        meopen = valves[me][0] * (remaining-1) if me in useful and me not in used else 0
        elopen = valves[elephant][0] * (remaining-1) if elephant in useful and elephant not in used and me != elephant else 0
        
        if meopen or elopen:
            newused = list(used)
            if meopen:
                newused.append(me)
            if elopen:
                newused.append(elephant)
            heappush(frontier, [remaining-1, score + meopen + elopen, valve, elephant, newused])

        for u in useful:
            for v in useful:
                if u in used and v in used:
                    continue

                if u == valve and v == valve:
                    continue

                taking = max(distances[me][u], distances[elephant][v])
                arrival = remaining-taking

                if arrival > 0:
                    newused = list(used)
                    if u not in newused:
                        newused.append(u)
                    if v not in newused:
                        newused.append(v)

                    t = tuple(newused)

                    if t not in paths:
                        paths.add(t)
                        heappush(frontier, [arrival, score, u, v, list(used)])
    
    return highest
        


def main():
    lines = []

    with open('16.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
