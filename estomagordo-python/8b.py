from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives


def solve(lines):
    height = len(lines)
    width = len(lines[0])

    best = 0
    
    for y in range(height):
        for x in range(width):
            n = y
            s = height-y-1
            w = x
            e = width-x-1

            h = lines[y][x]

            for dy in range(1, y+1):
                if lines[y-dy][x] >= h:
                    n = dy
                    break

            for dy in range(1, height-y):
                if lines[y+dy][x] >= h:
                    s = dy
                    break

            for dx in range(1, x+1):
                if lines[y][x-dx] >= h:
                    w = dx
                    break

            for dx in range(1, width-x):
                if lines[y][x+dx] >= h:
                    e = dx
                    break

            best = max(best, n*s*w*e)

    return best


def main():
    lines = []

    with open('8.txt') as f:
        for line in f.readlines():
            lines.append(digits(line))
            
    return solve(lines)


if __name__ == '__main__':
    print(main())

# 1495728