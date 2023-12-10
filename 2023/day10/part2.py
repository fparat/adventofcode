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


PIPE = {
    NODE_NS: "│",
    NODE_EW: "─",
    NODE_NE: "└",
    NODE_NW: "┘",
    NODE_SW: "┐",
    NODE_SE: "┌",
}

PIPE_LOOP = {
    NODE_NS: "┃",
    NODE_EW: "━",
    NODE_NE: "┗",
    NODE_NW: "┛",
    NODE_SW: "┓",
    NODE_SE: "┏",
}

def print_pretty(grid):
    for r, row in enumerate(grid):
        for c, node in enumerate(row):
            if isinstance(node, Node2):
                if node.is_loop:
                    print(PIPE_LOOP.get(node.value, node.value), end="")
                elif node.color == "O":
                    print(" ", end="")
                elif node.color != "O":
                    print("I", end="")
                else:
                    print(PIPE.get(node.value, node.value), end="")
            else:
                print(PIPE.get(node, node), end="")
        print()


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
    color = None

    @property
    def value(self):
        if self._value is not None:
            return self._value
        return self.grid[self.row][self.col]

    def __hash__(self):
        return hash((self.row, self.col))

    def neighbours(self):
        cls = self.__class__
        # visit north
        if self.value in [NODE_NS, NODE_NE, NODE_NW]:
            if (self.row - 1) >= 0:
                yield cls(self.grid, self.row - 1, self.col)
        # visit east
        if self.value in [NODE_EW, NODE_NE, NODE_SE]:
            if (self.col + 1) < len(self.grid[0]):
                yield cls(self.grid, self.row, self.col + 1)
        # visit south
        if self.value in [NODE_SE, NODE_SW, NODE_NS]:
            if (self.row + 1) < len(self.grid):
                yield cls(self.grid, self.row + 1, self.col)
        # visit west
        if self.value in [NODE_EW, NODE_NW, NODE_SW]:
            if (self.col - 1) >= 0:
                yield cls(self.grid, self.row, self.col - 1)


@dataclasses.dataclass
class Node2(Node):
    color = None
    is_loop = False

    def __hash__(self):
        return hash((self.row, self.col))


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

    def bfs(start: Union[Node, Node2]):
        explored = set()
        parents = {}
        q = deque()
        explored.add(start)
        q.append(start)
        while q:
            node: Node = q.popleft()
            yield node, node.row, node.col, parents
            for n in node.neighbours():
                if n not in explored:
                    explored.add(n)
                    parents[n] = node
                    q.append(n)

    *_, (last_node, _, _, parents) = bfs(start)

    length = 0
    node = last_node
    while node in parents:
        node = parents[node]
        length += 1

    print(f"Part 1: {length}")

    # Part 2

    # scale grid x3 to be able to flood fill

    scaled_grid = []
    for r, row in enumerate(grid):
        scaled_rows = [[], [], []]
        for c, node in enumerate(row):
            node = node.replace(NODE_START, start.value)
            if node == NODE_GND:
                scaled_rows[0] += [NODE_GND, NODE_GND, NODE_GND]
                scaled_rows[1] += [NODE_GND, NODE_GND, NODE_GND]
                scaled_rows[2] += [NODE_GND, NODE_GND, NODE_GND]
            elif node == NODE_NS:
                scaled_rows[0] += [NODE_GND, NODE_NS,  NODE_GND]
                scaled_rows[1] += [NODE_GND, NODE_NS,  NODE_GND]
                scaled_rows[2] += [NODE_GND, NODE_NS,  NODE_GND]
            elif node == NODE_EW:
                scaled_rows[0] += [NODE_GND, NODE_GND, NODE_GND]
                scaled_rows[1] += [NODE_EW,  NODE_EW,  NODE_EW]
                scaled_rows[2] += [NODE_GND, NODE_GND, NODE_GND]
            elif node == NODE_NE:
                scaled_rows[0] += [NODE_GND, NODE_NS,  NODE_GND]
                scaled_rows[1] += [NODE_GND, NODE_NE,  NODE_EW]
                scaled_rows[2] += [NODE_GND, NODE_GND, NODE_GND]
            elif node == NODE_NW:
                scaled_rows[0] += [NODE_GND, NODE_NS,  NODE_GND]
                scaled_rows[1] += [NODE_EW,  NODE_NW,  NODE_GND]
                scaled_rows[2] += [NODE_GND, NODE_GND, NODE_GND]
            elif node == NODE_SW:
                scaled_rows[0] += [NODE_GND, NODE_GND, NODE_GND]
                scaled_rows[1] += [NODE_EW,  NODE_SW,  NODE_GND]
                scaled_rows[2] += [NODE_GND, NODE_NS,  NODE_GND]
            elif node == NODE_SE:
                scaled_rows[0] += [NODE_GND, NODE_GND, NODE_GND]
                scaled_rows[1] += [NODE_GND, NODE_SE,  NODE_EW]
                scaled_rows[2] += [NODE_GND, NODE_NS,  NODE_GND]
            else:
                assert False

        scaled_grid.append(scaled_rows[0])
        scaled_grid.append(scaled_rows[1])
        scaled_grid.append(scaled_rows[2])

    scaled_start = (start.row * 3) + 1, (start.col * 3) + 1

    scaled_nodes = [[Node2(scaled_grid, r, c) for c, _ in enumerate(scaled_grid)] for r, row in enumerate(scaled_grid)]

    for _, r, c, _ in bfs(scaled_nodes[scaled_start[0]][scaled_start[1]]):
        scaled_nodes[r][c].is_loop = True

    # fill from top-left corner

    def flood_fill(start: Node2):
        q = deque()
        q.append(start)
        while q:
            node: Node2 = q.popleft()
            if node.is_loop or node.color is not None:
                continue
            node.color = "O"
            for (dr, dc) in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
                r, c = node.row + dr, node.col + dc
                if 0 <= r < len(node.grid) and 0 <= c < len(node.grid[0]):
                    q.append(scaled_nodes[r][c])

    flood_fill(scaled_nodes[0][0])

    unscaled_nodes = [[node for node in row[1::3]] for row in scaled_nodes[1::3]]

    inside = sum(not n.is_loop and n.color != "O" for row in unscaled_nodes for n in row)

    print(f"Part 2: {inside}")
