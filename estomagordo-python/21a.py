from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import adjacent, chunks, chunks_with_overlap, columns, custsort, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(lines):
    monkeys = {}

    for line in lines:
        parts = line.split()

        monkey = parts[0][:-1]
        pieces = []

        if len(parts) == 2:
            pieces.append(int(parts[1]))
        else:
            pieces += parts[1:]

        monkeys[monkey] = pieces

    while len(monkeys['root']) > 1:
        for k in monkeys.keys():
            v = monkeys[k]

            if len(v) == 1:
                continue

            if not isinstance(v[0], int):
                if len(monkeys[v[0]]) == 1:
                    v[0] = monkeys[v[0]][0]
            if not isinstance(v[2], int):
                if len(monkeys[v[2]]) == 1:
                    v[2] = monkeys[v[2]][0]

            op = v[1]

            if isinstance(v[0], int) and isinstance(v[2], int):
                a = v[0]
                b = v[2]
                val = 0

                if op == '+':
                    val = a+b
                elif op == '-':
                    val = a-b
                elif op == '/':
                    val = a//b
                else:
                    val = a*b

                monkeys[k] = [val]

    return monkeys['root'][0]

def main():
    lines = []

    with open('21.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
