from collections import deque
from copy import copy
from dataclasses import dataclass
from functools import cached_property
from itertools import permutations
from pathlib import Path
import re

import numpy as np
from rich import print
from rich.progress import track


def puzzle1(input_file: Path):
    def new_viable_states(state: "State", world: "World"):
        return [
            State(
                idx,
                time_left,
                state.pressure_released + flow * time_left,
                state.open_valve_indices | {idx},
            )
            for idx, flow in world.valve_index_to_flow_rate_mapping.items()
            if idx not in state.open_valve_indices
            if flow != 0
            if (
                time_left := (
                    state.time_left
                    - world.distance_matrix[state.cur_valve_idx, idx]
                    - 1
                )
            )
            >= 0
        ]

    world = World.from_input_file(input_file)
    start_state = State(
        cur_valve_idx=world.valve_to_index[world.start_valve],
        time_left=30,
        pressure_released=0,
    )
    stack = deque((start_state,))
    end_states: deque["State"] = deque()
    while stack:
        cur_state = stack.pop()
        new_states = new_viable_states(cur_state, world)
        if not new_states:
            end_states.append(cur_state)
        for state in new_states:
            stack.append(state)
    print(len(end_states))
    return max(s.pressure_released for s in end_states)


def puzzle2(input_file: Path):
    def new_viable_states(state: "State", world: "World"):
        return [
            State(
                idx,
                time_left,
                state.pressure_released + flow * time_left,
                state.open_valve_indices | {idx},
            )
            for idx, flow in world.valve_index_to_flow_rate_mapping.items()
            if idx not in state.open_valve_indices
            if flow != 0
            if (
                time_left := (
                    state.time_left
                    - world.distance_matrix[state.cur_valve_idx, idx]
                    - 1
                )
            )
            >= 0
        ]

    world = World.from_input_file(input_file)
    start_state = State(
        cur_valve_idx=world.valve_to_index[world.start_valve],
        time_left=26,
        pressure_released=0,
    )
    stack = deque((start_state,))
    end_states: deque["State"] = deque()
    while stack:
        cur_state = stack.pop()
        new_states = new_viable_states(cur_state, world)
        end_states.append(cur_state)
        for state in new_states:
            stack.append(state)

    end_states_sorted = sorted(
        end_states, key=lambda state: state.pressure_released, reverse=True
    )
    max_pressure = 0
    for i, state1 in track(enumerate(end_states_sorted), total=len(end_states_sorted)):
        for state2 in [*end_states_sorted[:i], *end_states_sorted[i:]]:
            if state1.pressure_released + state2.pressure_released <= max_pressure:
                break
            if state1.open_valve_indices.intersection(state2.open_valve_indices) == {0}:
                max_pressure = state1.pressure_released + state2.pressure_released
    return max_pressure


class State:
    def __init__(
        self,
        cur_valve_idx: int,
        time_left: int,
        pressure_released: int,
        open_valve_indices: set[int] | None = None,
    ) -> None:

        self.cur_valve_idx = cur_valve_idx
        self.time_left = time_left
        self.pressure_released = pressure_released

        if open_valve_indices is None:
            open_valve_indices = set()
        self.open_valve_indices = open_valve_indices
        self.open_valve_indices.add(cur_valve_idx)

    def __repr__(self) -> str:
        return (
            "State("
            + f"cur_valve_idx={self.cur_valve_idx}, "
            + f"time_left={self.time_left}, "
            + f"pressure_released={self.pressure_released}, "
            + f"open_valve_indices={self.open_valve_indices}"
            + ")"
        )


class World:
    INFINITY = 30_000

    def __init__(
        self,
        valve_to_flow_rate: dict[str, int],
        valve_to_paths: dict[str, list[str]],
        start_valve: str,
    ):
        self.valve_to_flow_rate = valve_to_flow_rate
        self.valve_to_paths = valve_to_paths
        self.start_valve = start_valve
        self.valve_to_index: dict[str, int] = {}
        self.index_to_valve: dict[int, str] = {}
        for idx, valve in enumerate(sorted(self.valve_to_flow_rate)):
            self.valve_to_index[valve] = idx
            self.index_to_valve[idx] = valve

    @classmethod
    def from_input_file(cls, input_file: Path):
        valve_to_flow_rate: dict[str, int] = {}
        valve_to_paths: dict[str, list[str]] = {}
        for valve, flow_rate, paths in _iter_inputs(input_file):
            valve_to_flow_rate[valve] = flow_rate
            valve_to_paths[valve] = paths

        return cls(
            valve_to_flow_rate=valve_to_flow_rate,
            valve_to_paths=valve_to_paths,
            start_valve="AA",
        )

    @cached_property
    def adjacency_matrix(self):
        num_valves = len(self.valve_to_paths)
        matrix = np.zeros((num_valves, num_valves), dtype=np.int32)
        for valve, idx in self.valve_to_index.items():
            for neighbor_valve in self.valve_to_paths[valve]:
                neighbor_idx = self.valve_to_index[neighbor_valve]
                matrix[idx, neighbor_idx] = 1
        return matrix

    @cached_property
    def distance_matrix(self):
        A = self.adjacency_matrix
        dist = np.where(A, A, self.INFINITY)
        np.fill_diagonal(dist, 0)
        num_valves = dist.shape[0]
        for k in range(num_valves):
            for r in range(num_valves):
                for c in range(num_valves):
                    if dist[r, c] > (new_shortest_dist := dist[r, k] + dist[k, c]):
                        dist[r, c] = new_shortest_dist
        return dist

    @cached_property
    def valve_index_to_flow_rate_mapping(self):
        return {
            i: self.valve_to_flow_rate[valve]
            for valve, i in self.valve_to_index.items()
        }


def _iter_inputs(input_file: Path):
    with open(input_file) as f:
        for line in f:
            yield _parse_line(line.rstrip())


def _parse_line(line: str):
    valve, *paths = re.findall(r" ([A-Z]+)", line)
    flow_rate = int(re.findall(r"flow rate=([0-9]+)", line)[0])
    return valve, flow_rate, paths


if __name__ == "__main__":
    print("Day 16")
    input_file = Path(__file__).parent / "input.txt"
    # input_file = Path(__file__).parent / "example_input.txt"
    # print("Puzzle 1:", puzzle1(input_file))
    print("Puzzle 2:", puzzle2(input_file))
