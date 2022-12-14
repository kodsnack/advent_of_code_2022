#!/usr/bin/env python3

# Day 7 2022: No Space Left On Device
# By Jakob Ruhe 2022-12-07

import os
import unittest


def parse_input(input):
    return input.strip().split("\n")


def chdir(cwd, path):
    if path == "/":
        return []
    elif path == "..":
        return cwd[0:-1]
    else:
        assert ".." not in path
        return cwd + path.split("/")


def add_file(root, cwd, name, size):
    directory = root
    for e in cwd:
        if e not in directory:
            directory[e] = {}
        directory = directory[e]
    directory[name] = size


def calc_size(directories, path, directory):
    size = 0
    for k, v in directory.items():
        if isinstance(v, dict):
            size += calc_size(directories, path + "/" + k, v)
        else:
            size += v
    directories[path if path else "/"] = size
    return size


def build_tree(entries):
    cwd = []
    root = {}
    for e in entries:
        elems = e.split(" ")
        if elems[0] == "$" and elems[1] == "cd":
            cwd = chdir(cwd, elems[2])
        elif elems[0] == "$" and elems[1] == "ls":
            pass
        elif elems[0] == "dir":
            pass
        else:
            add_file(root, cwd, elems[1], int(elems[0]))
    return root


def solve1(entries):
    root = build_tree(entries)
    directories = {}
    calc_size(directories, "", root)
    return sum([v for v in directories.values() if v <= 100000])


def solve2(entries):
    root = build_tree(entries)
    directories = {}
    calc_size(directories, "/", root)

    used = directories["/"]
    total = 70000000
    unused = total - used
    need_to_delete = 30000000 - unused
    assert need_to_delete > 0
    return min([v for v in directories.values() if v >= need_to_delete])


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 95437)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 24933642)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
