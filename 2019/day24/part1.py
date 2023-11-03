#!/usr/bin/env python3

import sys
from typing import *


Bugs = Set[Tuple[int, int]]


WIDTH = None
HEIGHT = None


def parse_bugs(s: str) -> Bugs:
    bugs = set()
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c == '#':
                bugs.add((x, y))
    return bugs


def cycle(bugs: Bugs) -> Bugs:
    new_bugs = set(bugs)
    assert id(new_bugs) != id(bugs)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            neighbours = 0
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if (x+dx, y+dy) in bugs:
                    neighbours += 1
            if (x, y) in bugs:
                if neighbours != 1:
                    new_bugs.remove((x, y))
            else:
                if neighbours == 1 or neighbours == 2:
                    new_bugs.add((x, y))
    return new_bugs


def rating(bugs: Bugs) -> int:
    r = 0
    for y in range(WIDTH):
        for x in range(HEIGHT):
            if (x, y) in bugs:
                r += pow(2, y * WIDTH + x)
    return r


def draw(bugs: Bugs):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            print('#' if (x, y) in bugs else '.', end='')
        print('\n', end='')
    print(flush=True)


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    WIDTH = len(inp.splitlines()[0])
    HEIGHT = len(inp.splitlines())

    # Part 1

    bugs = parse_bugs(inp)
    layouts = set([frozenset(bugs)])

    while True:
        bugs = cycle(bugs)
        if bugs in layouts:
            print(f"Part 1: {rating(bugs)}")
            break
        layouts.add(frozenset(bugs))
