from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(groups):
    monkeys = []

    for group in groups:
        handles = 0
        items = ints(group[1])
        op = group[2].split()
        addition = op[-2] == '+'
        opval = -1 if op[-1] == 'old' else int(op[-1])
        div = int(group[3].split()[-1])
        iftrue = int(group[4].split()[-1])
        iffalse = int(group[5].split()[-1])

        monkeys.append([handles, items, addition, opval, div, iftrue, iffalse])

    rounds = 20

    for _ in range(rounds):
        for monkey in monkeys:
            handles, items, addition, opval, div, iftrue, iffalse = monkey

            for item in items:
                monkey[0] += 1

                selfing = opval == -1

                if addition and selfing:
                    item *= 2
                elif addition:
                    item += opval
                elif selfing:
                    item *= item
                else:
                    item *= opval

                item//= 3

                if item % div == 0:
                    monkeys[iftrue][1].append(item)
                else:
                    monkeys[iffalse][1].append(item)

            monkey[1] = []

    handles = [monkey[0] for monkey in monkeys]
    handles.sort()

    return handles[-2] * handles[-1]                


def main():
    lines = []

    with open('11.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(grouped_lines(lines))


if __name__ == '__main__':
    print(main())