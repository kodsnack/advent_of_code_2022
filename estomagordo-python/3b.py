from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded


def solve(lines):
    s = 0
    m = len(lines)

    for x in range(0, m, 3):
        o, p, q = lines[x:x+3]

        c = [x for x in o if x in p and x in q][0]

        if c.isupper():
            s += 27 + ord(c)-ord('A')
        else:
            s += 1 + ord(c)-ord('a')

    return s


def main():
    lines = []

    with open('3.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
