from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from helpers import adjacent, chunks, chunks_with_overlap, columns, custsort, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


class Node:
    def __init__(self, val):
        self.next = None
        self.prev = None
        self.val = val


def solve(lines):
    first = None
    back = None
    zero = None
    nodes = []
    key = 811589153

    for line in lines:
        val = int(line) * key
        node = Node(val)

        if val == 0:
            zero = node

        if back:
            back.next = node
            node.prev = back
        else:
            first = node

        back = node
        nodes.append(node)

    first.prev = node
    node.next = first

    for i in range(10):
        print(i)
        for node in nodes:
            steps = node.val % (len(nodes) - 1)
            moving = node

            if steps == 0:
                continue
            if steps == 1:
                next = node.next
                nextnext = node.next.next
                prev = node.prev

                node.next = nextnext
                node.prev = next
                next.next = node
                next.prev = prev
                nextnext.prev = node
                prev.next = next

                continue
            if steps == len(nodes) - 1:
                next = node.next
                prev = node.prev
                prevprev = node.prev.prev

                node.next = prev
                node.prev = prevprev
                next.prev = prev
                prev.next = next
                prev.prev = node
                prevprev.next = node
                
                continue
            
            for x in range(steps):
                moving = moving.next

            endprev = moving
            endnext = moving.next
            
            startprev = node.prev
            startnext = node.next
            startprev.next = startnext
            startnext.prev = startprev
            endprev.next = node
            endnext.prev = node
            node.prev = endprev
            node.next = endnext
        
    s = 0
    moving = zero

    for x in range(3000):
        moving = moving.next

        if x % 1000 == 999:
            s += moving.val
                    
    return s                


def main():
    lines = []

    with open('20.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
