from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve(lines):
    pairs = grouped_lines(lines)

    pairs.append(['[[2]]', '[[6]]'])

    def parse(seq):
        l = []
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

    l = []

    for a, b in pairs:
        l.append(parse(a))
        l.append(parse(b))

    def mergesort(l):
        n = len(l)

        if n < 2:
            return l

        a = l[:n//2]
        b = l[n//2:]

        ll = []

        la = len(a)
        lb = len(b)
        pa = 0
        pb = 0
        sa = mergesort(a)
        sb = mergesort(b)

        while pa < la and pb < lb:
            comp = compare_element(sa[pa], sb[pb])

            if comp == -1:
                ll.append(sb[pb])
                pb += 1
            else:
                ll.append(sa[pa])
                pa += 1

        while pa < la:
            ll.append(sa[pa])
            pa += 1
        while pb < lb:
            ll.append(sb[pb])
            pb += 1

        return ll

    l = mergesort(l)

    # i = 0
    # while i < len(l):
    #     for j in range(i+1, len(l)):
    #         comp = compare_element(l[i], l[j])
    #         if comp == -1:
    #             l[i], l[j] = l[j], l[i]
    #             i = -1
    #             break
    #     i += 1

    # l.sort(key=compare_element)

    m = 1
    print(len(l))

    for i, el in enumerate(l):
        if el in ([[[2]]], [[[6]]]):
            print(i, el)
            m *= (i+1)

    return m


def main():
    lines = []

    with open('13.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())

# 90902