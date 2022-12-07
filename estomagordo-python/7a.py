from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives


def solve(lines):
    limit = 100000
    root = [{}, {}, None]
    filesystem = {'/': root}
    directory = filesystem['/']

    for line in lines:
        command = line.rstrip().split()

        if command[0] == '$':

            if command[1] == 'cd':
                if command[2] == '..':
                    directory = directory[2]
                elif command[2] == '/':
                    directory = root
                else:
                    directory = directory[0][command[2]]
            if command[1] == 'ls':
                pass

        if command[0].isdigit():
            directory[1][command[1]] = int(command[0])

        if command[0] == 'dir':
            if command[1] not in directory[0]:
                newdir = [{}, {}, directory]
                filesystem[command[1]] = newdir
                directory[0][command[1]] = newdir

    def size(directory):
        subdirs, files, _ = filesystem[directory]

        return sum(v for v in files.values()) + sum(size(subdir) for subdir in subdirs)
    
    sizes = {directory: size(directory) for directory in filesystem.keys()}

    return sum(s for s in sizes.values() if s <= limit)


def main():
    lines = []

    with open('7.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())

# 1248154
# 1177658
# 1383008