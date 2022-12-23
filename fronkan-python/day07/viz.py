from pathlib import Path
from collections import defaultdict

from rich.tree import Tree
from rich import print


def render_tree(tree, rich_tree):
    for a, b in tree.items():
        if isinstance(b, dict):
            render_tree(b, rich_tree.add(a))
        else:
            rich_tree.add(f"{a}: {b}")
    return rich_tree


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
    input_file = Path(__file__).parent / "input.txt"
    # input_file = Path(__file__).parent / "example_input.txt"
    print(
        render_tree(
            _build_tree_dict(input_file),
            Tree("/"),
        )
    )
