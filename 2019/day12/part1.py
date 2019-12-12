#!/usr/bin/env python3
# coding: utf-8

import re
import itertools
from dataclasses import dataclass
from typing import NamedTuple


@dataclass
class ThreeDimension:
    x: int = 0
    y: int = 0
    z: int = 0

    def abs_sum(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    @classmethod
    def from_str(cls, s):
        """`<x=2, y=-10, z=-7>` -> `cls(2, -10, -7)`"""
        m = re.search(r"<x=([-\d]+),\s*y=([-\d]+),\s*z=([-\d+]+)>", s)
        if m is None:
            raise ValueError(f"Input format not recognized: {s!r}")
        else:
            return cls(*map(int, m.groups()))


class Position(ThreeDimension):
    pass


class Velocity(ThreeDimension):
    pass


@dataclass
class Moon:
    pos: Position
    vel: Velocity

    def potential_energy(self):
        return self.pos.abs_sum()

    def kinetic_energy(self):
        return self.vel.abs_sum()

    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()


class Simulation:
    def __init__(self, moons=()):
        self.moons = list(moons)

    @classmethod
    def from_str(cls, s):
        moons = [Moon(Position.from_str(l), Velocity()) for l in s.splitlines()]
        return cls(moons)

    def __repr__(self):
        moon_repr = repr(self.moons).replace('Position', '').replace('Velocity', '')
        return f"Simulation({moon_repr})".replace("Moon", "\nMoon")

    def apply_gravity(self):
        for a, b in itertools.combinations(self.moons, 2):
            for d in "xyz":
                if getattr(a.pos, d) < getattr(b.pos, d):
                    setattr(a.vel, d, getattr(a.vel, d) + 1)
                    setattr(b.vel, d, getattr(b.vel, d) - 1)
                elif getattr(a.pos, d) > getattr(b.pos, d):
                    setattr(a.vel, d, getattr(a.vel, d) - 1)
                    setattr(b.vel, d, getattr(b.vel, d) + 1)

    def apply_velocity(self):
        for moon in self.moons:
            moon.pos.x += moon.vel.x
            moon.pos.y += moon.vel.y
            moon.pos.z += moon.vel.z

    def step(self):
        self.apply_gravity()
        self.apply_velocity()

    def total_energy(self):
        return sum(moon.total_energy() for moon in self.moons)


def main():
    with open("input") as f:
        sim = Simulation.from_str(f.read())

    for step in range(1000):
        sim.step()

    print(f"Total energy: {sim.total_energy()}")


if __name__ == "__main__":
    main()
