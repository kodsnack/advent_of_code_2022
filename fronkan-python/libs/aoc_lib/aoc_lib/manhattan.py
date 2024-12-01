

def abs_manhattan_distance_nd(pos1, pos2):
    assert len(pos1) == len(pos2)
    return sum([
        abs(pos1[i] - pos2[i])
        for i in range(len(pos1))
    ])

def abs_manhattan_distance(pos1, pos2):
    return sum([
        abs(pos1[0] - pos2[0]),
        abs(pos1[1] - pos2[1])
    ])

def cells_within_manhattan_distance(pos, dist, *, inclusive=False):
    if inclusive:
        y_start = pos[1]-dist
        y_end = pos[1] + (dist+1)
    else:
        y_start = pos[1] - (dist - 1)
        y_end = pos[1] + dist 
    mod_start = y_start- pos[1]

    for modifier, y in enumerate(range(y_start, y_end), start=mod_start):
        for x in _x_within_manhattan_distance(pos[0], dist, abs(modifier), inclusive=inclusive):
            yield (x,y)


def _x_within_manhattan_distance(x_pos, dist, row_modifier, *, inclusive=False):
    if inclusive:
        x_start = x_pos - dist + row_modifier
        x_end = x_pos + (dist+1) - row_modifier
    else:
        x_start = x_pos - (dist-1) + row_modifier
        x_end = x_pos + dist - row_modifier

    for x in range(x_start, x_end):
        yield x
