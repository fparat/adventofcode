#!/usr/bin/env python3

import sys

class HMap:
    def __init__(self, hmap):
        self.hmap = hmap

    @classmethod
    def from_file(cls, f):
        with open(filename) as f:
            hmap = [[int(d) for d in line.strip()] for line in f]
        return cls(hmap)

    def __iter__(self):
        for row, line in enumerate(self.hmap):
            for col, h in enumerate(line):
                yield (row, col), h

    def neighbors(self, row, col):
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if 0 <= row+dr < len(self.hmap) and 0 <= col+dc < len(self.hmap[0]):
                yield self.hmap[row+dr][col+dc]


def part1(hmap):
    result = 0
    for (row, col), h in hmap:
        if all(h < n for n in hmap.neighbors(row, col)):
            result += h + 1
    print(f"Part 1: {result}")


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    hmap = HMap.from_file(filename)

    part1(hmap)
