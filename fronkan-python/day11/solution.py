from pathlib import Path
from typing import Callable, NewType, Self
from collections import deque
import operator as op

import numpy as np

from aoc_lib.input_readers import read_chunks
from aoc_lib.maths import prod

MonkeyID = int
WorryLevel = int

OPS = {
    "*": np.multiply,
    "+": np.add,
}


def puzzle1(input_file: Path):
    monkeys = [
        parse_monkey(monkey_chunk)
        for monkey_chunk in read_chunks(input_file)
    ]
    for _ in range(1, 21):
        for cur_monkey in sorted(monkeys):
            cur_monkey.inspect_all()
            cur_monkey.calm_down()
            cur_monkey.throw_all(monkeys)
        print(_, *[m for m in monkeys], "-" * 80, sep="\n")

    return monkey_business(monkeys)


def puzzle2(input_file: Path):
    monkeys = [
        parse_monkey(monkey_chunk)
        for monkey_chunk in read_chunks(input_file)
    ]
    lowest_common_div = np.lcm.reduce([m.test.div for m in monkeys])
    for _ in range(1, 10_001):
        for cur_monkey in sorted(monkeys):
            cur_monkey.items = cur_monkey.items % lowest_common_div
            cur_monkey.inspect_all()
            cur_monkey.throw_all(monkeys)
    return monkey_business(monkeys)


class Test:
    def __init__(
        self, div: int, monkey_true: MonkeyID, monkey_false: MonkeyID
    ) -> None:
        self.div = div
        self.monkey_true = monkey_true
        self.monkey_false = monkey_false

    def __call__(self, items: np.ndarray) -> np.ndarray:
        res = np.array([self.monkey_true for _ in items])
        res[items % self.div != 0] = self.monkey_false
        return res


class Monkey:
    def __init__(
        self,
        _id: MonkeyID,
        items: np.ndarray,
        inspect_op: Callable[[np.ndarray], np.ndarray],
        test: Test,
    ) -> None:
        self._id = _id
        self.items = items
        self.inspect_op = inspect_op
        self.test = test
        self.items_thrown = 0

    def __repr__(self):
        return (
            "<Monkey("
            + f"id={self.id}, "
            + f"items={list(self.items)}, "
            + f"items_thrown={self.items_thrown}, "
            + f"inspect_op=..., "
            + f"test=..."
            + ")>"
        )

    def __lt__(self, other):
        if not isinstance(other, Monkey):
            raise ValueError("Can only compare to other monkeys")
        return self.id < other.id

    @property
    def id(self):
        return self._id

    def inspect_all(self):
        self.items = self.inspect_op(self.items)

    def calm_down(self):
        self.items = self.items // 3

    def throw_all(self, others: list["Monkey"]):
        receivers = self.decide_receiver()
        self.items_thrown += len(self.items)
        monkey_true = others[self.test.monkey_true]
        monkey_true.items = np.append(
            monkey_true.items, self.items[receivers == self.test.monkey_true]
        )

        monkey_false = others[self.test.monkey_false]
        monkey_false.items = np.append(
            monkey_false.items, self.items[receivers == self.test.monkey_false]
        )
        self.items = np.array([], dtype=np.int64)

    def decide_receiver(self):
        return self.test(self.items)


def parse_monkey(monkey_chunk: list[str]) -> Monkey:
    monkey_id = int(monkey_chunk[0].rstrip(": \n").split()[-1])

    item_str = monkey_chunk[1].split(":")[-1]
    items = np.array([int(elem) for elem in item_str.split(",")], dtype=np.int64)

    operation = _parse_operations(monkey_chunk[2].split(":")[-1])

    test_mod_condition = int(monkey_chunk[3].split(" ")[-1])

    assert monkey_chunk[4].lstrip().startswith("If true")
    monkey_true = int(monkey_chunk[4].split()[-1])

    assert monkey_chunk[5].lstrip().startswith("If false")
    monkey_false = int(monkey_chunk[5].split()[-1])

    return Monkey(
        _id=monkey_id,
        items=items,
        inspect_op=operation,
        test=Test(test_mod_condition, monkey_true, monkey_false),
    )


def _parse_operations(op_instr: str):
    operation = op_instr.split("=")[-1].strip()
    arg1, operator, arg2 = operation.split()
    assert not arg1.isnumeric()
    if arg2.isnumeric():
        return lambda var: OPS[operator](var, int(arg2))
    else:
        return lambda var: OPS[operator](var, var)


def monkey_business(monkeys):
    return prod(
        sorted((monkey.items_thrown for monkey in monkeys), reverse=True)[:2]
    )


if __name__ == "__main__":
    print("Day 11")
    input_file = Path(__file__).parent / "input.txt"
    # input_file = Path(__file__).parent / "example_input.txt"
    print("Puzzle 1:", puzzle1(input_file))
    print("Puzzle 2:", puzzle2(input_file))
