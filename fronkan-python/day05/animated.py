from contextlib import contextmanager
from pathlib import Path
import time
from typing import Self
from itertools import takewhile

from rich.console import Console, Group
from rich.live import Live
from rich.columns import Columns
from rich.panel import Panel


def _parse_input(input_file: Path):
    with open(input_file) as f:
        lines = iter(f)
        stack_lines = list(takewhile(lambda row: row.strip() != "", lines))
        moves = [Move.from_move_instruction(l.strip()) for l in lines]
    stacks = _parse_stacks(stack_lines)
    return stacks, moves


class Move:
    def __init__(self, num_blocks: int, start_stack: int, stop_stack: int) -> None:
        self.num_blocks = num_blocks
        self.start_stack = start_stack
        self.stop_stack = stop_stack

    @classmethod
    def from_move_instruction(cls: Self, move_instruction: str) -> Self:
        ops = move_instruction.split()
        return cls(
            num_blocks=int(ops[1]),
            start_stack=int(ops[3]),
            stop_stack=int(ops[5]),
        )

    def __repr__(self) -> str:
        return f"Move(num_blocks={self.num_blocks}, start_stack={self.start_stack}, stop_stack={self.stop_stack})"


def _parse_stacks(stacks_lines):
    stack_indices = [int(num) for num in _parse_stack_line(stacks_lines[-1])]
    stacks = {idx: [] for idx in stack_indices}
    for line in reversed(stacks_lines[:-1]):
        cells = _parse_stack_line(line)
        for stack_id, cell in zip(stacks, cells, strict=True):
            if _is_block(cell):
                stacks[stack_id].append(cell)
    return stacks


def _parse_stack_line(line):
    line = line.rstrip("\n")
    i = 0
    blocks = []
    while i <= len(line):
        blocks.append(line[i : i + 3])
        i += 4
    return blocks


def _is_block(cell: str):
    return cell.strip() != ""


BEAT_TIME = 0.04


@contextmanager
def beat(length: int = 1) -> None:
    yield
    time.sleep(length * BEAT_TIME)


def _render_stacks(stacks, console: Console):
    cols = []
    for k, stack in stacks.items():
        if not stack:
            continue
        cols.append(
            Columns(
                [
                    Panel(str(k), style="red", padding=(0, 0)),
                    *(Panel(block.strip("[]"), padding=(0, 0)) for block in stack),
                ],
                expand=False,
            )
        )
    console.print(Panel(Group(*cols)))


def _stacks_panel(stacks):
    cols = []
    for k, stack in stacks.items():
        # if not stack:
        #     continue
        cols.append(
            Columns(
                [
                    Panel(str(k), style="red", padding=(0, 0)),
                    *(Panel(block.strip("[]"), padding=(0, 0)) for block in stack),
                ],
                padding=(0, 0),
            )
        )
    return Panel(Group(*cols))


if __name__ == "__main__":
    input_file = Path(__file__).parent / "input.txt"
    stacks, moves = _parse_input(input_file)
    console = Console()
    console.clear()
    p = _stacks_panel(stacks)
    with Live(p, console=console, screen=False, refresh_per_second=30) as live:
        for move in moves:
            time.sleep(0.2)
            cur_stack = stacks[move.start_stack]
            moved_stack = cur_stack[-move.num_blocks :]
            stacks[move.start_stack] = cur_stack[: -move.num_blocks]
            stacks[move.stop_stack] += reversed(moved_stack)
            live.update(_stacks_panel(stacks))

    _render_stacks(stacks, console)
