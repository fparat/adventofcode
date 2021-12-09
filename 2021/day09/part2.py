#!/usr/bin/env python3

import sys
import math
from collections import deque
from functools import reduce

class HMap:
    def __init__(self, hmap):
        self.hmap = hmap
        self.filled = [[0 for _ in l] for l in self.hmap]
        self.bassins = []

    @classmethod
    def from_file(cls, f):
        with open(filename) as f:
            hmap = [[int(d) for d in line.strip()] for line in f]
        return cls(hmap)

    def __iter__(self):
        for row, line in enumerate(self.hmap):
            for col, h in enumerate(line):
                yield (row, col), h

    def __contains__(self, item):
        row, col = item
        return 0 <= row < len(self.hmap) and 0 <= col < len(self.hmap[0])

    def neighbors(self, row, col):
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if (row+dr, col+dc) in self:
                yield self.hmap[row+dr][col+dc]

    def lowpoints(self):
        for (row, col), h in self:
            if all(h < n for n in self.neighbors(row, col)):
                yield (row, col), h

    def find_bassins(self):
        bassins = []

        # Flood fill algorithm
        for (row, col), _ in self.lowpoints():
            filled = [[0 for _ in l] for l in self.hmap]
            q = deque()
            q.append((row, col))
            while q:
                r, c = q.popleft()
                if (r, c) not in self:
                    continue
                if not filled[r][c] and self.hmap[r][c] < 9:
                    filled[r][c] = 1
                    q.append((r+1, c))
                    q.append((r-1, c))
                    q.append((r, c+1))
                    q.append((r, c-1))

            bassins.append(sum(sum(l) for l in filled))

        return bassins

def part1(hmap):
    result = sum(h + 1 for _, h in hmap.lowpoints())
    print(f"Part 1: {result}")


def part2(hmap):
    bassins = hmap.find_bassins()
    result = math.prod(sorted(bassins)[-3:])
    print(f"Part 2: {result}")


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    hmap = HMap.from_file(filename)

    part1(hmap)
    part2(hmap)
