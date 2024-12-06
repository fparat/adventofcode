#!/usr/bin/env python3

import sys

GUARD = "^"
OBSTACLE = "#"

# (dy, dx)
N = (-1, 0)
S = (1, 0)
E = (0, 1)
W = (0, -1)

ROT90 = { N: E, E: S, S: W, W: N }


def find_guard(grid):
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == GUARD:
                return (y, x, N)


def step(grid, guard, obstacle = None):
    def peek():
        peeky = guard[0] + guard[2][0]
        peekx = guard[1] + guard[2][1]
        return peeky, peekx

    peeky, peekx = peek()

    if peeky < 0 or peeky >= len(grid) or peekx < 0 or peekx >= len(grid[0]):
        return None

    while grid[peeky][peekx] == OBSTACLE or (peeky, peekx) == obstacle:
        guard = (guard[0], guard[1], ROT90[guard[2]])
        peeky, peekx = peek()

    return (
        guard[0] + guard[2][0],
        guard[1] + guard[2][1],
        guard[2],
    )


def is_loop(grid, guard, obstacle):
    visited = set([guard])
    while (guard := step(grid, guard, obstacle)) is not None:
        if guard in visited:
            return True
        visited.add(guard)
    return False


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    grid = [list(line) for line in inp.splitlines()]
    guard = find_guard(grid)
    visited = set([guard[0:2]])

    while (guard := step(grid, guard)) is not None:
        visited.add(guard[0:2])

    print(f"Part 1: {len(visited)}")

    # Part 2

    guard_start = find_guard(grid)
    loops = sum(is_loop(grid, guard_start, v) for v in visited)
    print(f"Part 2: {loops}")
