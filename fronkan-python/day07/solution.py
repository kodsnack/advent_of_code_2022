from pathlib import Path
from collections import defaultdict


def puzzle1(input_file: Path):
    tree = _build_tree_dict(input_file)
    return sum(v for v in _calc_size(tree, defaultdict(int)).values() if v <= 10_0000)


def puzzle2(input_file: Path):
    MAX_SIZE = 70_000_000
    UPDATE_SIZE = 30_000_000
    tree = _build_tree_dict(input_file)
    path_to_sizes = _calc_size(tree, defaultdict(int))
    total_unused_space = MAX_SIZE - path_to_sizes["/"]
    min_to_delete = UPDATE_SIZE - total_unused_space
    assert min_to_delete > 0
    for dir_size in sorted(path_to_sizes.values()):
        if dir_size > min_to_delete:
            return dir_size
    raise RuntimeError("No way to free up enough space, we are doomed")


def _calc_size(tree, path_to_size: defaultdict[str, int], dir_path=""):
    parent_folder = dir_path if dir_path else "/"
    for k, v in tree.items():
        if isinstance(v, dict):
            _calc_size(v, path_to_size, f"{dir_path}/{k}")
            path_to_size[parent_folder] += path_to_size[f"{dir_path}/{k}"]
        else:

            path_to_size[parent_folder] += v
    return path_to_size


def _build_tree_dict(input_file: Path):
    tree = _empty_tree_dict()
    cur_dir = Path("/")
    for line in input_file.read_text().splitlines():
        tokens = line.split()
        if _is_command(tokens):
            _, cmd, *attrs = tokens
            if cmd == "cd":
                if attrs[0] == "/":
                    cur_dir = Path("/")
                elif attrs[0] == "..":
                    cur_dir = cur_dir.parent
                else:
                    cur_dir = cur_dir / attrs[0]
            elif cmd == "ls":
                pass
            else:
                raise ValueError(f"Failed parsing command: {line}")
        else:
            tree_path = [p for p in str(cur_dir).split("/") if p]
            target_dir = tree
            for p in tree_path:
                target_dir = target_dir[p]
            if tokens[0] == "dir":
                target_dir[tokens[1]] = _empty_tree_dict()
            else:
                target_dir[tokens[1]] = int(tokens[0])

    return tree


def _is_command(tokens: list[str]):
    return tokens[0] == "$"


def _empty_tree_dict():
    return defaultdict(_empty_tree_dict)


if __name__ == "__main__":
    print("Day 7")
    input_file = Path(__file__).parent / "input.txt"
    # input_file = Path(__file__).parent / "example_input.txt"
    print("Puzzle 1:", puzzle1(input_file))
    print("Puzzle 2:", puzzle2(input_file))
