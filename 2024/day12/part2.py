#!/usr/bin/env python3

import sys
from dataclasses import dataclass


@dataclass
class Zone:
    type: str
    plots: list[tuple[int, int]]
    perimeter: int = 0
    sides: int = 0


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

    # Part 2

    def grid_get(y, x):
        if y not in range(len(grid)) or x not in range(len(grid[0])):
            return None
        try:
            return grid[y][x]
        except IndexError:
            return None

    def calc_sides(zone):
        sides = 0
        for y, x in zone.plots:
            # check corners
            n = (y - 1, x) in zone.plots
            e = (y, x + 1) in zone.plots
            s = (y + 1, x) in zone.plots
            w = (y, x - 1) in zone.plots
            sides += n == w and (y - 1, x - 1) not in zone.plots or n == w == False
            sides += n == e and (y - 1, x + 1) not in zone.plots or n == e == False
            sides += s == e and (y + 1, x + 1) not in zone.plots or s == e == False
            sides += s == w and (y + 1, x - 1) not in zone.plots or s == w == False
        return sides

    for zone in zones:
        zone.sides = calc_sides(zone)

    print(f"Part 2: {sum(len(zone.plots) * zone.sides for zone in zones)}")
