from pathlib import Path


def puzzle1(input_file: Path):
    return puzzle1_main(input_file.read_text().strip())


def puzzle1_main(signal: str) -> int:
    return _find_unique_window(signal, 4)


def puzzle2(input_file: Path):
    return puzzle2_main(input_file.read_text().strip())


def puzzle2_main(signal: str) -> int:
    return _find_unique_window(signal, 14)


def _find_unique_window(signal: str, window_size: int):
    window = []
    for count, char in enumerate(signal, start=1):
        if char not in window:
            window = [*window[-(window_size - 1) :], char]
        else:
            dupe_idx = window.index(char)
            window = [*window[dupe_idx + 1 :], char]

        if len(set(window)) == window_size:
            return count


if __name__ == "__main__":
    print("Day 6")
    input_file = Path(__file__).parent / "input.txt"
    print("Puzzle 1:", puzzle1(input_file))
    print("Puzzle 2:", puzzle2(input_file))
