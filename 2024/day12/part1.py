#!/usr/bin/env python3

import sys
from collections import namedtuple
from dataclasses import dataclass


Zone = namedtuple("Zone", ["type", "plots", "perimeter"])


@dataclass
class Zone:
    type: str
    plots: list[tuple[int, int]]
    perimeter: int = None


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    grid = [list(line) for line in inp.splitlines()]

    zones = []
    index = {}

    def explore(zone, y, x):
        zone.plots.append((y, x))
        index[y, x] = zone
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            if ny not in range(len(grid)) or nx not in range(len(grid[0])):
                # zone.perimeter += 1
                continue
            if grid[ny][nx] != zone.type:
                # if id(index.get((ny, nx))) != id(zone):
                #     zone.perimeter += 1
                continue
            if (ny, nx) in index:
                continue
            explore(zone, ny, nx)

    def calc_perimeter(zone):
        perimeter = 0
        for ploty, plotx in zone.plots:
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = ploty + dy, plotx + dx
                if (ny, nx) not in zone.plots:
                    perimeter += 1
        return perimeter

    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if (y, x) in index:
                continue
            zone = Zone(c, [], 0)
            explore(zone, y, x)
            zones.append(zone)
            zone.perimeter = calc_perimeter(zone)

    print(f"Part 1: {sum(len(zone.plots) * zone.perimeter for zone in zones)}")
