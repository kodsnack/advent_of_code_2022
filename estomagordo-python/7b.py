from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives


def solve(lines):
    root = [{}, {}, None, '/']
    directory = root

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
                newdir = [{}, {}, directory, directory[3] + command[1] + '/']
                directory[0][command[1]] = newdir

    sizes = {}

    def sizeup(directory):
        subdirs, files, _, name = directory

        totsize = sum(v for v in files.values()) + sum(sizeup(subdir) for subdir in subdirs.values())
        sizes[name] = totsize

        return totsize
    
    sizeup(root)

    space = 70000000
    needmax = 30000000
    need = space - needmax
    using = sizes['/']  
    
    best = 10**10

    for size in sizes.values():
        if using - size <= need:
            best = min(best, size)

    return best


def main():
    lines = []

    with open('7.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())