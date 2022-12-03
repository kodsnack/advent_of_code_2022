import pathlib

def get_input():
    input = pathlib.Path('input.txt').read_text().splitlines()
    return input


def part1(input):
    calories = []
    elf_calories = 0

    for line in input:
        if line:
            elf_calories += int(line)
        else:
            calories.append(elf_calories)
            elf_calories = 0

    return max(calories)


def part2(input):
    calories = []
    elf_calories = 0

    for line in input:
        if line:
            elf_calories += int(line)
        else:
            calories.append(elf_calories)
            elf_calories = 0

    calories.sort()
    return sum(calories[-3:])


input = get_input()
print(f"Part 1: {part1(input)}")
print(f"Part 2: {part2(input)}")
