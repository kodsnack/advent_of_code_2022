from aoc_lib.manhattan import cells_within_manhattan_distance, abs_manhattan_distance
from aoc_lib.maths import clamp


pos = (5,5)
for dist in range(0, 10):
    res = list(cells_within_manhattan_distance(pos, dist, inclusive=True))

    for cell in res:
        assert abs_manhattan_distance(cell, pos) <= dist, "incl"


pos = (5,5)
for dist in range(0, 10):
    res = list(cells_within_manhattan_distance(pos, dist))

    for cell in res:
        assert abs_manhattan_distance(cell, pos) <= dist, "not inclusive"


pos = (5,5)
for dist in range(0, 10):
    res = list(cells_within_manhattan_distance(pos, dist, inclusive=False))
    for cell in res:
        assert abs_manhattan_distance(cell, pos) < dist, f"derp: {cell=}, {dist=}"


import numpy as np 

a = np.zeros((10,10), dtype=np.int8)
for cell in cells_within_manhattan_distance(pos, 3, inclusive=False):
    a[(cell[1], cell[0])] = 1

print(*["".join(str(c) for c in row) for row in a], sep="\n")
print("-"*80)

a = np.zeros((10,10), dtype=np.int8)
for cell in cells_within_manhattan_distance(pos, 3, inclusive=True):
    a[(cell[1], cell[0])] = 1

print(*["".join(str(c) for c in row) for row in a], sep="\n")


def _edge_nodes(center_pos, dist, max_size):
    center_x, center_y = center_pos
    y_start = clamp(center_y-dist, 0, max_size)
    y_end = clamp(center_y + (dist+1), 0, max_size)
    mod_start = y_start-center_y
    for row_modifier, y in enumerate(range(y_start, y_end), start=mod_start):
        x_left = center_x - dist + abs(row_modifier)
        if 0 <= x_left <= max_size:
            yield (x_left,y)
        
        x_right = center_x + (dist) - abs(row_modifier)
        if x_right != x_left and 0 <= x_right <= max_size:
            yield (x_right,y)


b = np.zeros((10,10), dtype=np.int8)
b[pos] = 2
for cell in _edge_nodes(pos, 4, max_size=10):
    b[(cell[1], cell[0])] = 3

print(*["".join(str(c) for c in row) for row in a+b], sep="\n")
