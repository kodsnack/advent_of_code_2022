from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives


def solve(lines):
    height = len(lines)
    width = len(lines[0])

    visible = set()

    

    for y in range(height):
        highest = -1

        for x in range(width):
            if lines[y][x] > highest:
                visible.add((y, x))
            highest = max(highest, lines[y][x])

        highest = -1

        for x in range(width-1, -1, -1):
            if lines[y][x] > highest:
                visible.add((y, x))
            highest = max(highest, lines[y][x])

    for x in range(width):
        highest = -1

        for y in range(height):
            if lines[y][x] > highest:
                visible.add((y, x))
            highest = max(highest, lines[y][x])

        highest = -1

        for y in range(height-1, -1, -1):
            if lines[y][x] > highest:
                visible.add((y, x))
            highest = max(highest, lines[y][x])

    # for y in range(height):
    #     for x in range(width):
    #         if (y, x) not in visible:
    #             print(y, x)

    return len(visible)


def main():
    lines = []

    with open('8.txt') as f:
        for line in f.readlines():
            lines.append(digits(line))
            
    return solve(lines)


if __name__ == '__main__':
    print(main())

# 352