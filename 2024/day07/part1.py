#!/usr/bin/env python3

import sys
import itertools
from operator import add, mul


def calc(vals, ops):
    ival = iter(vals)
    res = next(ival)
    for op in ops:
        res = op(res, next(ival))
    assert next(ival, None) is None
    return res


def is_solvable(eq):
    test, vals = eq
    numops = len(vals) - 1
    for bitperm in range(2**numops):
        ops = [[add, mul][(bitperm >> i) & 1] for i in range(numops)]
        if calc(vals, ops) == test:
            return True
    return False


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    equations = [
        (int(test), [int(v) for v in vals.split()])
        for (test, vals) in (line.split(":") for line in inp.splitlines())
    ]

    part1 = sum(eq[0] for eq in equations if is_solvable(eq))

    print(f"Part 1: {part1}")
