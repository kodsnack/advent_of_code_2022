from pathlib import Path
from ast import literal_eval
from functools import cmp_to_key

from aoc_lib.input_readers import read_chunks


def puzzle1(input_file: Path):
    indices = []
    for idx, packet_pair in enumerate(read_chunks(input_file), start=1):
        raw_packet1, raw_packet2 = packet_pair
        packet1 = literal_eval(raw_packet1.strip())
        packet2 = literal_eval(raw_packet2.strip())

        res = compare(packet1, packet2)
        if res < 0:
            indices.append(idx)
    return sum(indices)


def puzzle2(input_file: Path):
    div_pack1 = [[2]]
    div_pack2 = [[6]]
    packets = [
        literal_eval(clean_line)
        for line in input_file.read_text().splitlines()
        if (clean_line := line.strip())
    ]
    packets.extend([div_pack1, div_pack2])

    res = 1
    for idx, packet in enumerate(sorted(packets, key=cmp_to_key(compare)), start=1):
        if packet == div_pack1 or packet == div_pack2:
            res *= idx
    return res


def compare(p1, p2):
    match (p1, p2):
        case int(), list():
            return compare_lists_less_than([p1], p2)
        case list(), list():
            return compare_lists_less_than(p1, p2)
        case list(), int():
            return compare_lists_less_than(p1, [p2])
        case int(), int():
            if p1 == p2:
                return 0
            if p1 < p2:
                return -1
            if p1 > p2:
                return 1
    raise TypeError(
        f"Expected p1 and p2 to be list or int but got: {type(p1)} and {type(p2)}"
    )


def compare_lists_less_than(p1, p2):
    while p1 and p2:
        v1, p1 = p1[0], p1[1:]
        v2, p2 = p2[0], p2[1:]
        res: int = compare(v1, v2)
        if res != 0:
            return res

    if len(p1) <= len(p2):
        return -1
    if len(p1) > len(p2):
        return 1
    return 0


if __name__ == "__main__":
    print("Day 13")
    input_file = Path(__file__).parent / "input.txt"
    # input_file = Path(__file__).parent / "example_input.txt"
    print("Puzzle 1:", puzzle1(input_file))
    print("Puzzle 2:", puzzle2(input_file))
