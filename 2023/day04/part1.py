#!/usr/bin/env python3

import sys

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    part1 = 0
    for line in inp.splitlines():
        winning, have = [set(int(n) for n in g.split()) for g in line.split(':')[1].split('|')]
        if (num := len(winning.intersection(have))) > 0:
            part1 += 1 << (num - 1)

    print(f"Part 1: {part1}")
