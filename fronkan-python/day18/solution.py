from collections import deque
from dataclasses import dataclass
from pathlib import Path
from ast import literal_eval

Voxel = tuple[int,int,int]

def puzzle1(input_file: Path):
    voxels: set[Voxel] = {literal_eval(row) for row in input_file.read_text().splitlines()}
    droplets = _find_disjunct_droplets(voxels)
    return sum(len(droplet.boundaries) for droplet in droplets)



def puzzle2(input_file: Path):
    lava_voxels: set[Voxel] = {literal_eval(row) for row in input_file.read_text().splitlines()}
    max_x = 0
    max_y = 0
    max_z = 0

    max_x = max(v[0] for v in lava_voxels) + 2
    max_y = max(v[1] for v in lava_voxels) + 2
    max_z = max(v[2] for v in lava_voxels) + 2
    min_x = min(v[0] for v in lava_voxels) - 2
    min_y = min(v[1] for v in lava_voxels) - 2
    min_z = min(v[2] for v in lava_voxels) - 2

    def _is_in_boundary(v: Voxel):
        if v[0] < min_x or v[1] < min_y or v[2] < min_z:
            return False
        if v[0] > max_x or v[1] > max_y or v[2] > max_z:
            return False
        return True

    stack = deque([(max_x, max_y, max_z)])
    visited = set()
    cnt = 0
    while stack:
        voxel = stack.pop()
        if voxel in lava_voxels:
            continue
        if voxel in visited:
            continue
        visited.add(voxel)
        neighbors = _neighboring_voxels_set(voxel)
        cnt += len(neighbors&lava_voxels)
        stack.extend({v for v in neighbors if _is_in_boundary(v)} - visited - lava_voxels)
    return cnt

@dataclass
class DisjunctDroplet:
    boundaries: list[Voxel]
    lava: set[Voxel]

def _find_disjunct_droplets(voxels: set[Voxel]):
    droplets: list[DisjunctDroplet] = []
    for voxel in voxels:
        matching_block_idx = [
            idx
            for idx, droplet in enumerate(droplets)
            if voxel in droplet.boundaries
        ]
        new_droplet = DisjunctDroplet(_neighboring_voxels(voxel), {voxel,})
        if matching_block_idx:
            for block_idx in reversed(matching_block_idx):
                matching_droplet = droplets[block_idx]
                new_droplet.boundaries += matching_droplet.boundaries
                new_droplet.lava |= matching_droplet.lava
                new_droplet.boundaries = [boundary for boundary in new_droplet.boundaries if boundary not in new_droplet.lava]
                del droplets[block_idx]

        droplets.append(new_droplet)
    return droplets


def _neighboring_voxels(voxel: Voxel) -> list[Voxel]:
    return [
        (voxel[0]-1, voxel[1], voxel[2]),
        (voxel[0]+1, voxel[1], voxel[2]),
        (voxel[0], voxel[1]-1, voxel[2]),
        (voxel[0], voxel[1]+1, voxel[2]),
        (voxel[0], voxel[1], voxel[2]-1),
        (voxel[0], voxel[1], voxel[2]+1),
    ]

def _neighboring_voxels_set(voxel: Voxel) -> set[Voxel]:
    return {
        (voxel[0]-1, voxel[1], voxel[2]),
        (voxel[0]+1, voxel[1], voxel[2]),
        (voxel[0], voxel[1]-1, voxel[2]),
        (voxel[0], voxel[1]+1, voxel[2]),
        (voxel[0], voxel[1], voxel[2]-1),
        (voxel[0], voxel[1], voxel[2]+1),
    }


if __name__ == "__main__":
    print("Day 18")
    input_file = Path(__file__).parent / "input.txt"
    # input_file = Path(__file__).parent / "example_input.txt"
    # print("Puzzle 1:", puzzle1(input_file))
    print("Puzzle 2:", puzzle2(input_file)) # TODO: 3818 to high, 2405 to low, not 3782, not 2832, not 2576