#!/usr/bin/env python3

import sys
import re

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1
    part1 = sum(int(m[1]) * int(m[2]) for m in re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)", inp))
    print(f"Part 1: {part1}")