from pathlib import Path


class InclusiveRange:
    def __init__(self, start: int, stop: int) -> None:
        if stop < start:
            raise ValueError(f"Stop must be less than start, got {start=}, {stop=}")
        self.start = start
        self.stop = stop

    def __len__(self):
        return (self.stop - self.start) + 1

    def __repr__(self) -> str:
        return f"InclusiveRange(start={self.start},stop={self.stop})"

    def __contains__(self, item: int):
        return self.start <= item <= self.stop


def puzzle1(input_file: Path):
    count = 0
    for elf1, elf2 in _iter_pair(input_file):
        start = min(elf1.start, elf2.start)
        stop = max(elf1.stop, elf2.stop)
        if len(InclusiveRange(start, stop)) == max(len(elf1), len(elf2)):
            count += 1
    return count


def puzzle2(input_file: Path):
    count = 0
    for elf1, elf2 in _iter_pair(input_file):
        if _is_overlap(elf1, elf2):
            count += 1
    return count


def _is_overlap(r1: InclusiveRange, r2: InclusiveRange):
    return any(
        (
            r1.start in r2,
            r1.stop in r2,
            r2.start in r1,
            r2.stop in r1,
        )
    )


def _iter_pair(input_file: Path):
    with open(input_file) as f:
        for line in f:
            r1, r2 = line.split(",")
            range1 = _parse_range(r1)
            range2 = _parse_range(r2)
            yield range1, range2


def _parse_range(range_str: str):
    start, end = range_str.split("-")
    return InclusiveRange(int(start), int(end))


if __name__ == "__main__":
    print("Day 4")
    input_file = Path(__file__).parent / "input.txt"
    # input_file = Path(__file__).parent / "example_input.txt"
    print("Puzzle 1:", puzzle1(input_file))
    print("Puzzle 2:", puzzle2(input_file))
