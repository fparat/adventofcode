#!/usr/bin/env python3

import sys
import dataclasses
from collections import deque
from typing import *


NODE_NS = "|"
NODE_EW = "-"
NODE_NE = "L"
NODE_NW = "J"
NODE_SW = "7"
NODE_SE = "F"
NODE_GND = "."
NODE_START = "S"


def find_start_pos(grid):
    for r, row in enumerate(grid):
        for c, node in enumerate(row):
            if node == NODE_START:
                # guess start pipe type
                has_north = grid[r-1][c] in [NODE_SE, NODE_SW, NODE_NS]
                has_south = grid[r+1][c] in [NODE_NS, NODE_NE, NODE_NW]
                has_west = grid[r][c-1] in [NODE_EW, NODE_NE, NODE_SE]
                has_east = grid[r][c+1] in [NODE_EW, NODE_NW, NODE_SW]
                match (has_north, has_south, has_west, has_east):
                    case (True,  True,  False, False): return Node(grid, r, c, NODE_NS)
                    case (False, False, True,  True):  return Node(grid, r, c, NODE_EW)
                    case (True,  False, False, True):  return Node(grid, r, c, NODE_NE)
                    case (True,  False, True,  False): return Node(grid, r, c, NODE_NW)
                    case (False, True,  True,  False): return Node(grid, r, c, NODE_SW)
                    case (False, True,  False, True):  return Node(grid, r, c, NODE_SE)
                    case _: assert False


@dataclasses.dataclass
class Node:
    grid: List[List[str]] = dataclasses.field(repr=False)
    row: int
    col: int
    _value: Optional[str] = None # forced for start

    @property
    def value(self):
        if self._value is not None:
            return self._value
        return self.grid[self.row][self.col]

    def __hash__(self):
        return hash((self.row, self.col))

    def neighbours(self):
        # visit north
        if self.value in [NODE_NS, NODE_NE, NODE_NW]:
            if (self.row - 1) >= 0:
                yield Node(self.grid, self.row - 1, self.col)
        # visit east
        if self.value in [NODE_EW, NODE_NE, NODE_SE]:
            if (self.col + 1) < len(self.grid[0]):
                yield Node(self.grid, self.row, self.col + 1)
        # visit south
        if self.value in [NODE_SE, NODE_SW, NODE_NS]:
            if (self.row + 1) < len(self.grid):
                yield Node(self.grid, self.row + 1, self.col)
        # visit west
        if self.value in [NODE_EW, NODE_NW, NODE_SW]:
            if (self.col - 1) >= 0:
                yield Node(self.grid, self.row, self.col - 1)


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    grid = [list(line) for line in inp.splitlines()]
    start = find_start_pos(grid)

    def bfs(start: Node):
        explored = set()
        parents = {}
        q = deque()
        explored.add(start)
        q.append(start)
        while q:
            node: Node = q.popleft()
            yield node, parents
            for n in node.neighbours():
                if n not in explored:
                    explored.add(n)
                    parents[n] = node
                    q.append(n)

    *_, (last_node, parents) = bfs(start)

    length = 0
    node = last_node
    while node in parents:
        node = parents[node]
        length += 1

    print(f"Part 1: {length}")
