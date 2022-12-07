from pathlib import Path
from string import ascii_lowercase, ascii_uppercase
from collections import deque, Counter

letter2value = {
    letter: value
    for value, letter in enumerate(ascii_lowercase + ascii_uppercase, start=1)
}


def puzzle1(input_file: Path):
    all_misplaced_letters = []
    for line in input_file.read_text().splitlines():
        line_center = len(line) // 2
        pocket1 = set(line[:line_center])
        pocket2 = set(line[line_center:])
        misplaced_items = pocket1 & pocket2
        assert len(misplaced_items) == 1
        all_misplaced_letters.append(misplaced_items.pop())
    return sum(letter2value[letter] for letter in all_misplaced_letters)


def puzzle2(input_file: Path):
    labels = []
    for group in _iter_groups(input_file):
        possible_labels = set.intersection(*(set(elf) for elf in group))
        assert len(possible_labels) == 1
        labels.append(possible_labels.pop())
    return sum(letter2value[label] for label in labels)


def _iter_groups(input_file: Path):
    lines = deque(input_file.read_text().splitlines())
    while lines:
        group = []
        while len(group) < 3:
            group.append(lines.popleft())
        yield group


if __name__ == "__main__":
    print("Day 3")
    input_file = Path(__file__).parent / "input.txt"
    # input_file = Path(__file__).parent / "example_input.txt"
    print("Puzzle 1:", puzzle1(input_file))
    print("Puzzle 2:", puzzle2(input_file))
