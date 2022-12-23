from enum import Enum
import functools
from pathlib import Path


@functools.total_ordering
class Hand:
    class Shape(Enum):
        ROCK = 1
        PAPER = 2
        SCISSORS = 3

        @classmethod
        def shapes(cls):
            if hasattr(cls, "_shape"):
                return cls._shape
            cls._shape = list(cls)
            return cls._shape

        def beating_shape(self):
            shapes = self.shapes()
            idx = self.value - 1
            beating_index = (idx + 1) % len(shapes)
            return shapes[beating_index]

        def loosing_shape(self):
            shapes = self.shapes()
            idx = self.value - 1
            loosing_index = idx - 1
            return shapes[loosing_index]

    def __init__(self, shape):
        self.shape = shape

    def __eq__(self, other):
        if not isinstance(other, Hand):
            raise TypeError(f"Can't compare Hand with type {type(other)}")
        return self.shape == other.shape

    def __lt__(self, other):
        if not isinstance(other, Hand):
            raise TypeError(f"Can't compare Hand with type {type(other)}")
        if other.shape == Hand.Shape.SCISSORS and self.shape == Hand.Shape.ROCK:
            return False
        elif self.shape == Hand.Shape.SCISSORS and other.shape == Hand.Shape.ROCK:
            return True
        else:
            return self.shape.value < other.shape.value

    @property
    def points(self):
        return self.shape.value

    def beating_hand(self):
        return Hand(Hand.Shape.beating_shape(self.shape))

    def loosing_hand(self):
        return Hand(Hand.Shape.loosing_shape(self.shape))

    def copy(self):
        return Hand(self.shape)


ELF_HANDS = {
    "A": Hand.Shape.ROCK,
    "B": Hand.Shape.PAPER,
    "C": Hand.Shape.SCISSORS,
}


def puzzle1(input_file: Path):
    player_hands = {
        "X": Hand.Shape.ROCK,
        "Y": Hand.Shape.PAPER,
        "Z": Hand.Shape.SCISSORS,
    }
    player_score = 0
    for row in input_file.read_text().splitlines():
        elf_letter, player_letter = row.split()
        elf_hand = Hand(ELF_HANDS[elf_letter])
        player_hand = Hand(player_hands[player_letter])

        player_score += player_hand.points

        if player_hand > elf_hand:
            player_score += 6
        elif player_hand == elf_hand:
            player_score += 3
    return player_score


def puzzle2(input_file: Path):
    player_score = 0
    for row in input_file.read_text().splitlines():
        elf_letter, player_letter = row.split()
        elf_hand = Hand(ELF_HANDS[elf_letter])

        if player_letter == "X":
            player_hand = elf_hand.loosing_hand()
        elif player_letter == "Y":
            player_hand = elf_hand.copy()
        elif player_letter == "Z":
            player_hand = elf_hand.beating_hand()
        else:
            raise ValueError(f"Unexpected player letter: {player_letter}")

        player_score += player_hand.points

        if player_hand > elf_hand:
            player_score += 6
        elif player_hand == elf_hand:
            player_score += 3
    return player_score


if __name__ == "__main__":
    print("Day 2")
    input_file = Path(__file__).parent / "input.txt"
    # input_file = Path(__file__).parent / "example_input.txt"
    print("Puzzle 1:", puzzle1(input_file))
    print("Puzzle 2:", puzzle2(input_file))
