#!/usr/bin/env python3
# coding: utf-8

import sys
import os
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


def run(s):
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

    def get_required_ore(element: Element) -> int:
        from math import ceil
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

        for reaction in reactions:
            if any(wanted.name == product.name for product in reaction.products):
                product = reaction.products[0]
                reaction_num = ceil(wanted.count / product.count)
                dprint(f"{reaction}  (x{reaction_num})")

                ores = 0
                for reactant in reaction.reactants:
                    if reactant.name == "ORE":
                        addores = reactant.count * reaction_num
                        dprint(f"add {addores} ORE")
                    else:
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

    return get_required_ore(fuel_reaction.products[0])


def test():
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


def main():
    with open("input") as f:
        print(run(f.read()))


if __name__ == "__main__":
    test()
    main()
