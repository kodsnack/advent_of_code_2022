from pathlib import Path

import numpy as np
from rich import print

def puzzle1(input_file: Path):
    head = np.array([0,0], dtype=np.int64)
    tail = np.array([0,0], dtype=np.int64)
    positions = [tail.copy()]

    for move in _iter_head_move_vectors(input_file):
        head += move
        tail = _calc_new_knot_pos(head, tail)
        positions.append(tail.copy())

    return np.unique(positions, axis=0).shape[0]
        
    
def puzzle2(input_file: Path):
    head = np.array([0,0], dtype=np.int64)
    rope = [
        np.array([0,0], dtype=np.int64)
        for i in range(9)
    ]
    positions = [rope[-1].copy()]

    for move in _iter_head_move_vectors(input_file):
        head += move
        leading_knot = head
        for idx, following_knot in enumerate(rope):
            new_pos = _calc_new_knot_pos(leading_knot, following_knot)
            leading_knot = new_pos
            rope[idx] = new_pos
        positions.append(rope[-1].copy())

    return np.unique(positions, axis=0).shape[0]



DIRECTION_VECTORS = {
    "R": np.array([1,0], dtype=np.int64),
    "U": np.array([0,1], dtype=np.int64),
    "L": np.array([-1,0], dtype=np.int64),
    "D": np.array([0,-1], dtype=np.int64),

}

def _iter_head_move_vectors(input_file: Path):
    with open(input_file) as f:
        for line in f:
            direction, steps = line.split()
            for _ in range(int(steps)):
                yield DIRECTION_VECTORS[direction].copy()

def _calc_new_knot_pos(leading_knot, following_knot):
    diff = leading_knot - following_knot
    new_pos = following_knot.copy()

    if np.abs(np.linalg.norm(diff)) >= 2: 
        if diff[0] != 0:
            new_pos[0] += 1 if diff[0] > 0 else -1
        
        if diff[1] != 0:
            new_pos[1] += 1 if diff[1] > 0 else -1
    return new_pos

if __name__ == "__main__":
    print("Day 9")
    input_file = Path(__file__).parent / "input.txt"
    # input_file = Path(__file__).parent / "example_input.txt"
    print("Puzzle 1:", puzzle1(input_file))
    print("Puzzle 2:", puzzle2(input_file))