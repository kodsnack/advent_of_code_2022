from pathlib import Path


def _noop():
    yield 0

def _addx(v: str):
    yield 0
    yield int(v)

COMMANDS = {
    "noop": _noop,
    "addx": _addx,
}


def puzzle1(input_file: Path):
    commands = input_file.read_text().splitlines()
    signal_strengths = []
    cycle = 0
    x_register = 1 
    for command in commands:
        cmd, *args = command.split()
        for v in COMMANDS[cmd](*args):
            cycle += 1
            if (cycle % 40) - 20  == 0:
                signal_strengths.append(cycle*x_register)
            x_register += int(v)
    return sum(signal_strengths)

def puzzle2(input_file: Path):
    commands = input_file.read_text().splitlines()
    rows = []
    cycle = 0
    x_register = 1
    row = [] 
    for command in commands:
        cmd, *args = command.split()
        for v in COMMANDS[cmd](*args):
            if x_register - 1 <= cycle%40 <= x_register + 1:
                row.append("#")
            else:
                row.append(".")
            cycle += 1
            if cycle%40 == 0:
                rows.append("".join(row))
                row = []
            x_register += int(v)
    return rows



if __name__ == "__main__":
    print("Day 10")
    input_file = Path(__file__).parent / "input.txt"
    # input_file = Path(__file__).parent / "example_input.txt"

    print("Puzzle 1:", puzzle1(input_file))
    print("Puzzle 2:", "\n".join(puzzle2(input_file)), sep="\n")