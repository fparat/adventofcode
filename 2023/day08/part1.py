#!/usr/bin/env python3

import sys
import re
import itertools


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    lines = inp.splitlines()
    instructions = [{"L": 0, "R": 1}[s] for s in lines[0]]

    network = {}
    for node, left, right in (re.match(r"(\w+)\s*=\s*\((\w+),\s*(\w+)\)\s*", line).groups() for line in lines[2:]):
        network[node] = (left, right)

    step = 0
    node = "AAA"
    instr = itertools.cycle(instructions)
    while node != "ZZZ":
        node = network[node][next(instr)]
        step += 1

    print(f"Part 1: {step}")
