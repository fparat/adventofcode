#!/usr/bin/env python3

import os

from collections import namedtuple
from dataclasses import dataclass
from typing import List

class Position(namedtuple("Position", ["x", "y", "z"])):
    def __repr__(self):
        return f"({self.x:+}, {self.y:+}, {self.z:+})"


def iter_pos(x_min, x_max, y_min, y_max, z_min, z_max):
    for z in range(z_min, z_max+1):
        for y in range(y_min, y_max+1):
            for x in range(x_min, x_max+1):
                yield Position(x, y, z)


def iter_neighbors(pos):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                if not (dx == 0 and dy == 0 and dz == 0):
                    yield Position(pos.x + dx, pos.y + dy, pos.z + dz)


@dataclass
class PocketDimension:
    cubes: List[Position]  # activated

    @classmethod
    def from_string(cls, s):
        cubes = []
        for row, line in enumerate(s.splitlines()):
            for col, c in enumerate(line.strip()):
                if c == '#':
                    cubes.append(Position(col, row, 0))
        return cls(cubes)

    @classmethod
    def from_file(cls, path):
        with open(path) as f:
            return cls.from_string(f.read())

    def is_active(self, x, y, z):
        return Position(x, y, z) in self.cubes

    def get_active_zone(self):
        x_min, x_max, y_min, y_max, z_min, z_max = 0, 0, 0, 0, 0, 0
        for pos in self.cubes:
            x_min, x_max = min(x_min, pos.x), max(x_max, pos.x)
            y_min, y_max = min(y_min, pos.y), max(y_max, pos.y)
            z_min, z_max = min(z_min, pos.z), max(z_max, pos.z)
        return x_min - 1, x_max + 1, y_min -1, y_max + 1, z_min - 1, z_max + 1

    def show(self):
        x_min, x_max, y_min, y_max, z_min, z_max = self.get_active_zone()
        for z in range(z_min, z_max+1):
            print(f"\nz={z}")
            for y in range(y_min, y_max+1):
                for x in range(x_min, x_max+1):
                    if self.is_active(x, y, z):
                        print("#", end="")
                    else:
                        print(".", end="")
                print("")
            print("")

    def active_cubes_num(self):
        return len(self.cubes)

    def active_neighbors_num(self, pos):
        assert len(list(iter_neighbors(pos))) == 26
        return sum(1 for neighbor in iter_neighbors(pos) if self.is_active(*neighbor))

    def cycle(self):
        zone = self.get_active_zone()
        next_cubes = []
        for pos in iter_pos(*zone):
            if self.is_active(*pos):
                if self.active_neighbors_num(pos) in [2, 3]:
                    next_cubes.append(pos)
            else:
                if self.active_neighbors_num(pos) == 3:
                    next_cubes.append(pos)
        self.cubes = next_cubes


def main():
    input_path = os.path.join(os.path.dirname(__file__), "input")
    pocket = PocketDimension.from_file(input_path)

    for _ in range(6):
        pocket.cycle()

    print(f"Part 1: {pocket.active_cubes_num()} active cubes")


if __name__ == "__main__":
    main()
