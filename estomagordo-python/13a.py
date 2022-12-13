from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(lines):
    pairs = grouped_lines(lines)

    def parse(seq):
        currseq = []
        stack = []
        currdig = ''

        for c in seq:
            if c.isdigit():
                currdig += c
            else:
                if currdig:
                    currseq.append(int(currdig))
                    currdig = ''
                if c == '[':
                    stack.append(currseq)
                    currseq = []
                if c == ']':
                    oldseq = stack.pop()
                    oldseq.append(currseq)
                    currseq = oldseq

        return currseq

    def compare_element(a, b):
        alist = isinstance(a, list)
        blist = isinstance(b, list)

        if alist and blist:
            for i, ael in enumerate(a):
                if i == len(b):
                    return -1

                comp = compare_element(ael, b[i])

                if comp != 0:
                    return comp

            if len(b) > len(a):
                return 1
            return 0
        elif alist:
            return compare_element(a, [b])
        elif blist:
            return compare_element([a], b)
        elif a < b:
            return 1
        elif a == b:
            return 0
        return -1

    def compare(a, b):
        pa = parse(a)
        pb = parse(b)

        return compare_element(pa, pb)

    s = 0

    for i, pair in enumerate(pairs):
        a, b = pair

        if compare(a, b) == 1:
            s += i+1

    return s


def main():
    lines = []

    with open('13.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
