#!/usr/bin/env python3

import sys
import itertools


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    grid = [list(line) for line in inp.splitlines()]

    freqs = {}
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c != '.':
                freqs.setdefault(c, []).append((y, x))

    antinodes = set()

    for freq, positions in freqs.items():
        for a, b in itertools.combinations(positions, 2):
            d = (b[0] - a[0], b[1] - a[1])
            low = (a[0] - d[0], a[1] - d[1])
            high = (b[0] + d[0], b[1] + d[1])
            if low[0] in range(0, len(grid)) and low[1] in range(0, len(grid[0])):
                antinodes.add(low)
            if high[0] in range(0, len(grid)) and high[1] in range(0, len(grid[0])):
                antinodes.add(high)

    print(f"Part 1: {len(antinodes)}")

    for freq, positions in freqs.items():
        for a, b in itertools.combinations(positions, 2):
            d = (b[0] - a[0], b[1] - a[1])
            antinode = a
            while True:
                if antinode[0] not in range(0, len(grid)) or antinode[1] not in range(0, len(grid[0])):
                    break
                antinodes.add(antinode)
                antinode = (antinode[0] + d[0], antinode[1] + d[1])
            antinode = a
            while True:
                if antinode[0] not in range(0, len(grid)) or antinode[1] not in range(0, len(grid[0])):
                    break
                antinodes.add(antinode)
                antinode = (antinode[0] - d[0], antinode[1] - d[1])

    print(f"Part 2: {len(antinodes)}")
