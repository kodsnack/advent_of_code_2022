from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives


def solve(lines):
    crates, moves = grouped_lines(lines)

    def stackify(crates):
        stacks = []

        for line in crates:
            n = len(line)

            for x in range(1, n, 4):
                if not line[x].isalpha():
                    continue

                cratenum = x//4

                while len(stacks) < cratenum+1:
                    stacks.append([])

                stacks[cratenum] = [line[x]] + stacks[cratenum]

        return stacks

    def apply(stacks, moves):
        for move in moves:
            number, frm, to = ints(move)

            stacks[to-1].extend(stacks[frm-1][-number:])
            stacks[frm-1] = stacks[frm-1][:-number]
            
    stacks = stackify(crates)
    apply(stacks, moves)   

    return ''.join(stack[-1] for stack in stacks)


def main():
    lines = []

    with open('5.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
