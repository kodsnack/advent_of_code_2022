from pathlib import Path
from itertools import islice

from aoc_lib.input_readers import read_chunks


def puzzle1(input_file: Path):
    elves = read_chunks(input_file)
    return max(_iter_calories_per_elf(elves))


def puzzle2(input_file: Path):
    elves = read_chunks(input_file)
    sorted_elves = sorted(_iter_calories_per_elf(elves), reverse=True)
    return sum(islice(sorted_elves, 3))


def _iter_calories_per_elf(elves):
    for elf in elves:
        yield sum(int(row) for row in elf)


if __name__ == "__main__":
    print("Day 1")
    input_file = Path(__file__).parent / "input.txt"
    # input_file = Path(__file__).parent / "example_input.txt"
    print("Puzzle 1:", puzzle1(input_file))
    print("Puzzle 2:", puzzle2(input_file))
