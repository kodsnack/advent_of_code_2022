import importlib
import pytest
from pathlib import Path

DIRECTORY = Path(__file__).parent

solution = importlib.import_module(f"{DIRECTORY.name}.solution")

def test_puzzle_1_example():
    input_file = Path(__file__).parent / "example_input.txt"
    res = solution._number_of_impossible_positions_on_line(input_file, 10)
    assert res == 26

def test_puzzle_2_example():
    input_file = Path(__file__).parent / "example_input.txt"
    res = solution._find_sos_beacon(input_file, 20)
    assert res == 56_000_011

@pytest.mark.parametrize(
    "puzzle, result",
    [
        (1, 4725496),
        (2, 12051287042458)
    ],
)
def test_puzzle_real_input(puzzle, result):
    input_file = Path(__file__).parent / "input.txt"
    puzzle_solver = getattr(solution, f"puzzle{puzzle}")
    assert puzzle_solver(input_file) == result