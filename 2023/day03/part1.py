#!/usr/bin/env python3

import sys
import string

NOT_SYMBOLS = string.digits + '.'


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    sch = inp.splitlines()

    # Find all numbers
    numbers = []
    for y, line in enumerate(sch):
        x = 0
        while x < len(line):
            if line[x].isdigit():
                d = line[x]
                x += 1
                while x < len(line) and line[x].isdigit():
                    d += line[x]
                    x += 1
                numbers.append((int(d), y, x - len(d), len(d)))
            else:
                x += 1

    # Select numbers that have an adjacent symbol

    def has_adjacent_symbol(y, x, l):
        # lines above and below the number
        for iy in [y-1, y+1]:
            if iy >= 0 and iy < len(sch):
                for ix in range(max(x-1, 0), min(x+l+1, len(sch[0]))):
                    if sch[iy][ix] not in NOT_SYMBOLS:
                        return True
        # chars before and after the number
        for ix in [x-1, x+l]:
            if ix >= 0 and ix < len(sch[0]):
                if sch[y][ix] not in NOT_SYMBOLS:
                    return True

    print(f"Part 1: {sum(n for n, y, x, l in numbers if has_adjacent_symbol(y, x, l))}")
