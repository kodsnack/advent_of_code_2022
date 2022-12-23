import numpy as np

def straight_lines(matrix: np.array, row_idx: int, col_idx: int):
    yield np.flip(matrix[:row_idx, col_idx])
    yield np.flip(matrix[row_idx, :col_idx])
    yield matrix[row_idx, col_idx + 1:]
    yield matrix[row_idx + 1:, col_idx]

def straight_lines_including_center(matrix: np.array, row_idx: int, col_idx: int):
    yield np.flip(matrix[:row_idx+1, col_idx].copy())
    yield np.flip(matrix[row_idx, :col_idx+1].copy())
    yield matrix[row_idx, col_idx:].copy()
    yield matrix[row_idx:, col_idx].copy()
