from collections import defaultdict
from pathlib import Path
import re

# from rich import print
from rich.progress import track

from aoc_lib.manhattan import abs_manhattan_distance, cells_within_manhattan_distance, _x_within_manhattan_distance
from aoc_lib.maths import clamp

def puzzle1(input_file: Path):
    return _number_of_impossible_positions_on_line(input_file, target_y=2_000_000)

def _number_of_impossible_positions_on_line(input_file: Path, target_y):
    impossible_x = set()
    for sensor_pos, beacon_pos in _sensor_beacon_pairs(input_file):
        dist = abs_manhattan_distance(sensor_pos, beacon_pos)
        sen_x, sen_y = sensor_pos

        if not ( (sen_y - dist) <= target_y <= (sen_y + dist)):
            continue

        row_modifier = abs(sen_y - target_y)
        for x in _x_within_manhattan_distance(sen_x, dist, row_modifier, inclusive=True):
            if (x,target_y) != sensor_pos and (x,target_y) != beacon_pos:
               impossible_x.add(x)
    return len(impossible_x)


def _sensor_beacon_pairs(input_file: Path):
    res = []
    for line in input_file.read_text().splitlines():
        sensor_info, beacon_info = re.findall(r"x=(-*[0-9]+), y=(-*[0-9]+)", line)
        sensor_pos = tuple(int(num) for num in sensor_info)
        beacon_pos = tuple(int(num) for num in beacon_info)
        res.append((sensor_pos, beacon_pos))
    return res


def puzzle2(input_file: Path):
    return _find_sos_beacon(input_file, 4_000_000)

def _find_sos_beacon(input_file: Path, max_size):
    sensor_beacon_pairs = _sensor_beacon_pairs(input_file)
    
    
    sensor_to_distance = {
        sensor_pos: abs_manhattan_distance(sensor_pos, beacon_pos)
        for sensor_pos, beacon_pos in sensor_beacon_pairs
    }
    for sensor_pos, dist in sensor_to_distance.items():
        edge_nodes = set(_edge_nodes(sensor_pos, dist+1, max_size))
        for node in edge_nodes:
            for sensor, no_touch_dist in sensor_to_distance.items():
                if abs_manhattan_distance(node, sensor) <= no_touch_dist:
                    break
            else:
                return node[0]*4_000_000 + node[1]
    



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




if __name__ == "__main__":
    print("Day 15")
    input_file = Path(__file__).parent / "input.txt"
    print("Puzzle 1:", puzzle1(input_file))
    print("Puzzle 2:", puzzle2(input_file))