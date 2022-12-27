from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import adjacent, chunks, chunks_with_overlap, columns, custsort, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(lines):
    def desnafu(snafu):
        val = 0
        base = 1

        for c in snafu[::-1]:
            if c.isdigit():
                val += base * int(c)
            elif c == '-':
                val -= base
            else:
                val -= 2 * base

            base *= 5

        return val

    s = 0

    for line in lines:
        n = desnafu(line.rstrip())
        s += n

        # print(line.rstrip(), n, s)

    startbase = 1
    while s >= 3 * startbase:
        startbase *= 5

    seen = {(s, startbase): (-1, -1)}
    frontier = deque([(s, startbase)])
    winner = (-1, -1)

    print(s)

    while frontier:
        n, base = frontier.popleft()
        
        if base == 1:
            s = ''
            if 0 <= n <= 2:
                s = str(n)
            if n == -1:
                s = '-'
            if n == -2:
                s = '='
            
            if s == '':
                continue

            winner = (n, base)
            break

        deltas = [2 * base, base, 0, -base, -2 * base]

        for d in deltas:
            if (n - d, base//5) in seen:
                continue

            if 3 * (base//5) < n - d:
                continue

            if 3 * (base//5) + (n - d) < 0:
                continue

            seen[(n-d, base//5)] = (n, base)

            if len(seen) % 1000000 == 0:
                print(len(seen), len(frontier))

            frontier.append((n-d, base//5))
    
    t = ''
    n, base = winner
    prev = 0

    while base != -1:
        diff = (n - prev) // base
        
        if diff >= 0:
            t += str(diff)
        elif diff == -2:
            t += '='
        else:
            t += '-'

        prev = n

        n, base = seen[(n, base)]

    return t[::-1]


def main():
    lines = []

    with open('25.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())