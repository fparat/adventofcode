#!/usr/bin/env python3
# coding: utf-8

import sys
import os
from math import ceil
from collections import namedtuple
from typing import NamedTuple, List, Dict, Optional

ENABLE_DEBUG = "-v" in sys.argv


class Element(NamedTuple):
    name: str
    count: int

    def __repr__(self):
        return f"{self.count}{self.name}"

    def __mul__(self, factor):
        assert isinstance(factor, int), "multiply with integer"
        return Element(self.name, self.count * factor)

    @classmethod
    def parse(cls, s: str) -> List["Element"]:
        elements = []
        for e in s.split(","):
            num, name = e.split()
            elements.append(Element(name.strip(), int(num)))
        return elements


class Reaction(NamedTuple):
    reactants: List[Element]
    products: List[Element]

    def __repr__(self):
        reactants = " + ".join(repr(reactant) for reactant in self.reactants)
        products = " + ".join(repr(product) for product in self.products)
        return f"{reactants} -> {products}"

    @classmethod
    def parse(cls, s: str) -> List["Reaction"]:
        reactions = []
        for line in s.splitlines():
            inp, out = line.split("=>")
            reactions.append(Reaction(Element.parse(inp), Element.parse(out)))
        return reactions


def run(s, target:Optional[Element]=None) -> [int, Dict[str, int]]:
    reactions = Reaction.parse(s)

    def find_fuel_raction(reactions) -> Optional[Reaction]:
        for reaction in reactions:
            for outputs in reaction[1]:
                if outputs[0].upper() == "FUEL":
                    return reaction
        return None

    fuel_reaction = find_fuel_raction(reactions)

    # Check assumptions
    assert all(len(reaction.products) == 1 for reaction in reactions)
    assert fuel_reaction.products[0].count == 1

    indent = 0

    def dprint(*args, **kwargs):
        """For debug prints"""
        if ENABLE_DEBUG:
            print(f"{' ' * indent}",  end="")
            print(*args, **kwargs)

    # Stash for keeping track of surplus
    stash = {}

    if target is None:
        target = Element("FUEL", 1)

    def get_required_ore(element: Element) -> int:
        nonlocal indent
        nonlocal stash
        indent += 2

        wanted = Element(*element)
        in_stash = stash.get(element.name, 0)
        if in_stash > 0:
            from_stash = min(in_stash, wanted.count)
            wanted = Element(wanted.name, wanted.count - from_stash)
            stash[element.name] -= from_stash
            dprint(f"take {from_stash} {wanted.name} from stash")
            dprint(stash)

        dprint(f"want {element}, actually {wanted}")

        if wanted.name == "ORE":
            return wanted.count

        for reaction in reactions:
            if any(wanted.name == product.name for product in reaction.products):
                product = reaction.products[0]
                reaction_num = ceil(wanted.count / product.count)
                dprint(f"{reaction}  (x{reaction_num})")

                ores = 0
                for reactant in reaction.reactants:
                    addores = get_required_ore(reactant * reaction_num)
                    dprint(f"add {addores} ORE*")
                    ores += addores

                surplus = (reaction_num * product.count) - wanted.count
                dprint(f'{surplus=}')
                if surplus > 0:
                    stash[wanted.name] = stash.get(wanted.name, 0) + surplus
                    dprint(f"surplus {surplus}{product.name} to stash: {stash}")

                indent -= 2
                return ores
        assert False, "must find ore"

    return get_required_ore(target)


def test1():
    TEST_CASES = [
        ("example1", 31),
        ("example2", 165),
        ("example3", 13312),
        ("example4", 180697),
        ("example5", 2210736),
    ]

    for f, expected in TEST_CASES:
        with open(f) as test_input:
            input_content = test_input.read()
        result = run(input_content)
        assert result == expected, f"'{f}' failed, expected {expected}, got {result}"
        print(f"{f} OK")


def part1():
    with open("input") as f:
        print(f"Part 1: {run(f.read())}")

TRILLION = 1000000000000

def run2(s):
    ore_per_fuel = run(s)
    fuel_max = ceil(TRILLION / ore_per_fuel)

    # We now we can at least produce fuel_max fuel with a trillion ore.
    # We can actually produce more because of the surplus
    # We do a binary search to find a better approximation

    range_min = fuel_max
    range_max = fuel_max * 2  # arbitrary
    while range_min < range_max:
        fuel = (range_min + range_max) // 2
        needed_ore = run(s, target=Element("FUEL", fuel))
        if needed_ore < TRILLION:
            range_min = fuel + 1
        elif needed_ore > TRILLION:
            range_max = fuel - 1
        else:
            # We used *exactly* 1 trillion ores
            return fuel

    # The binary search failed, because we cannot use exactly 1 trillion ores
    # but we found the amount of fuel +-1.
    while needed_ore < TRILLION:
        fuel += 1
        needed_ore = run(s, target=Element("FUEL", fuel))
    while needed_ore > TRILLION:
        fuel -= 1
        needed_ore = run(s, target=Element("FUEL", fuel))
    return fuel


def test2():
    TEST_CASES = [
        ("example3", 82892753),
        ("example4", 5586022),
        ("example5", 460664),
    ]

    for f, expected in TEST_CASES:
        with open(f) as test_input:
            input_content = test_input.read()
        fuel = run2(input_content)
        assert fuel == expected
        print(f"{f} OK")


def part2():
    with open("input") as f:
        print(f"Part 2: {run2(f.read())}")

if __name__ == "__main__":
    print("Part 1")
    test1()
    part1()

    print("Part 2")
    test2()
    part2()
