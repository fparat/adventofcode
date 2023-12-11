#!/usr/bin/env python3

import sys
import itertools


def expand(grid):
    grid = [row[:] for row in grid] # deep copy

    # expand vertically
    grid2 = []
    for row in grid:
        if all(c == "." for c in row):
            grid2.append(row[:])
        grid2.append(row)

    # expand horizontally
    expand_cols = []
    for i in range(len(grid2[0])):
        if all(row[i] == "." for row in grid2):
            expand_cols.append(i)
    for col in reversed(expand_cols):
        for row in grid2:
            row.insert(col, ".")

    return grid2


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    grid = [list(row) for row in inp.splitlines()]
    grid_exp = expand(grid)
    galaxies_exp = [(r, c) for r, row in enumerate(grid_exp) for c, v in enumerate(row) if v == "#"]

    result = 0
    for (r1, c1), (r2, c2) in set(tuple(sorted(pair)) for pair in itertools.permutations(galaxies_exp, r=2)):
        result += abs(r2 - r1) + abs(c2 - c1)

    print(f"Part 1: {result}")

    # Part 2

    expanded_rows = []
    for r, row in enumerate(grid):
        if all(c == "." for c in row):
            expanded_rows.append(r)

    expanded_cols = []
    for i in range(len(grid[0])):
        if all(row[i] == "." for row in grid):
            expanded_cols.append(i)

    galaxies = [(r, c) for r, row in enumerate(grid) for c, v in enumerate(row) if v == "#"]

    result = 0
    for (r1, c1), (r2, c2) in set(tuple(sorted(pair)) for pair in itertools.permutations(galaxies, r=2)):
        exp_rows = [r for r in expanded_rows if r in range(min(r1, r2), max(r1, r2) + 1)]
        exp_cols = [c for c in expanded_cols if c in range(min(c1, c2), max(c1, c2) + 1)]
        result += abs(r2 - r1) + abs(c2 - c1) + ((len(exp_rows) + len(exp_cols)) * (1000000 - 1))

    print(f"Part 2: {result}")
