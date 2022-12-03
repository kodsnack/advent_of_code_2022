from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded


def solve(lines):
    s = 0

    for l in lines:
        n = len(l)
        a = l[:n//2]
        b = l[n//2:]

        c = [x for x in a if x in b][0]

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
