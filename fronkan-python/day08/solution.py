from pathlib import Path

import numpy as np

from aoc_lib.np_grid import straight_lines

def puzzle1(input_file: Path):
    trees = np.array(
        [
            [int(height) for height in tree_line]
            for tree_line in input_file.read_text().splitlines()
        ]
    )
    visible_trees = np.zeros_like(trees)
    visible_trees[0, :] = 1
    visible_trees[-1, :] = 1
    visible_trees[:, 0] = 1
    visible_trees[:, -1] = 1

    len_rows, len_cols = trees.shape
    for row_idx in range(1, len_rows - 1):
        for col_idx in range(1, len_cols - 1):
            val = trees[row_idx, col_idx]
            for line in straight_lines(trees, row_idx, col_idx):
                if np.all(line < val):
                    visible_trees[row_idx, col_idx] = 1
                    break
    return visible_trees.sum()


def puzzle2(input_file: Path):
    trees = np.array(
        [
            [int(height) for height in tree_line]
            for tree_line in input_file.read_text().splitlines()
        ]
    )
    scores = np.zeros_like(trees)

    len_rows, len_cols = trees.shape
    for row_idx in range(1, len_rows - 1):
        for col_idx in range(1, len_cols - 1):
            val = trees[row_idx, col_idx]
            sight_line_lengths = [
                _len_sight_line(val, line)
                for line in straight_lines(trees, row_idx, col_idx)
            ]
            scores[row_idx, col_idx] = np.prod(sight_line_lengths)
    
    return scores.max()

def _len_sight_line(cur_tree_hight, sight_line):
    matches = np.where(sight_line >= cur_tree_hight)[0]
    len_sight_line = matches[0] + 1 if len(matches) else len(sight_line)
    return len_sight_line





if __name__ == "__main__":
    print("Day 8")
    input_file = Path(__file__).parent / "input.txt"
    # input_file = Path(__file__).parent / "example_input.txt"
    # print("Puzzle 1:", puzzle1(input_file))
    print("Puzzle 2:", puzzle2(input_file))

    # TODO: value to high (1_263_600)