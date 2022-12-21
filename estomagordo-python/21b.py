from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import adjacent, chunks, chunks_with_overlap, columns, custsort, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(lines):
    def prepmonkeys():
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

        haschanged = True
        while haschanged:
            haschanged = False

            for k in monkeys.keys():
                if k == 'humn':
                    continue

                v = monkeys[k]

                if len(v) == 1:
                    continue

                if not isinstance(v[0], int) and v[0] != 'humn':
                    if len(monkeys[v[0]]) == 1:
                        haschanged = True
                        v[0] = monkeys[v[0]][0]
                if not isinstance(v[2], int) and v[2] != 'humn':
                    if len(monkeys[v[2]]) == 1:
                        haschanged = True
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

        return monkeys

    monkeys = prepmonkeys()

    res = [v for v in monkeys['root'] if isinstance(v, int)][0]
    symbol = [v for v in monkeys['root'][0:3:2] if isinstance(v, str)][0]

    while symbol != 'humn':
        monkey = monkeys[symbol]
        val = [v for v in monkey if isinstance(v, int)][0]
        symbol = [v for v in monkey[0:3:2] if isinstance(v, str) and v != '+'][0]
        op = monkey[1]

        leftval = monkey[0] == val

        if op == '+':
            res -= val
        elif op == '-':
            if leftval:
                res = val - res
            else:
                res += val
        elif op == '/':
            if leftval:
                res = val // res
            else:
                res *= val
        else:
            res //= val

    return res


def main():
    lines = []

    with open('21.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())