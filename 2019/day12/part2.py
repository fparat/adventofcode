#!/usr/bin/env python3
# coding: utf-8

import re
import itertools
import math
from dataclasses import dataclass
from functools import reduce


@dataclass
class ThreeDimension:
    x: int = 0
    y: int = 0
    z: int = 0

    def dimension(self, dimension):
        return getattr(self, dimension)

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

    def find_period(self):
        periods = []
        for d in "xyz":
            def get_state():
                return [(moon.pos.dimension(d), moon.vel.dimension(d)) for moon in self.moons]
            initial = get_state()
            for step in itertools.count(1):
                self.step()
                state = get_state()
                if state == initial:
                    print(f"Found {step} for {d}")
                    periods.append(step)
                    break
        return lcm_reduce(*periods)


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def lcm_reduce(*values):
    return reduce(lcm, values)


def main():
    with open("input") as f:
        sim = Simulation.from_str(f.read())
    period = sim.find_period()
    print(f"Result: {period}")


if __name__ == "__main__":
    main()
