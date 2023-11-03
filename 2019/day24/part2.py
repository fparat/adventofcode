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


Bugs2 = Set[Tuple[int, int, int]]


def parse_bugs2(s: str) -> Bugs:
    return set([(0, x, y) for x, y in parse_bugs(s)])


def cycle2(bugs: Bugs2) -> Bugs2:
    new_bugs = set(bugs)
    level_min = min(level for level, _, _ in bugs)
    level_max = max(level for level, _, _ in bugs)
    for level in range(level_min-1, level_max+2):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if (x, y) == (2, 2):
                    continue
                neighbours = 0
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    before = neighbours
                    nx, ny = x+dx, y+dy

                    if nx == -1:
                        neighbours += int((level-1, 1, 2) in bugs)
                    elif nx == 5:
                        neighbours += int((level-1, 3, 2) in bugs)

                    if ny == -1:
                        neighbours += int((level-1, 2, 1) in bugs)
                    elif ny == 5:
                        neighbours += int((level-1, 2, 3) in bugs)

                    if (nx, ny) == (2, 2):
                        if (x, y) == (2, 1):
                            neighbours += sum(int((level+1, sx, 0) in bugs) for sx in range(WIDTH))
                        elif (x, y) == (3, 2):
                            neighbours += sum(int((level+1, 4, sy) in bugs) for sy in range(HEIGHT))
                        elif (x, y) == (2, 3):
                            neighbours += sum(int((level+1, sx, 4) in bugs) for sx in range(WIDTH))
                        elif (x, y) == (1, 2):
                            neighbours += sum(int((level+1, 0, sy) in bugs) for sy in range(HEIGHT))

                    if (level, x+dx, y+dy) in bugs:
                        neighbours += 1

                if (level, x, y) in bugs:
                    if neighbours != 1:
                        new_bugs.remove((level, x, y))
                else:
                    if neighbours == 1 or neighbours == 2:
                        new_bugs.add((level, x, y))
    return new_bugs


def draw2(bugs: Bugs2):
    level_min = min(level for level, _, _ in bugs)
    level_max = max(level for level, _, _ in bugs)
    for level in range(level_min, level_max+1):
        print(f"\nLevel {level}:")
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if (x, y) == (2, 2):
                    assert (level, x, y) not in bugs
                    print('?', end='')
                else:
                    print('#' if (level, x, y) in bugs else '.', end='')
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

    # Part 2

    bugs = parse_bugs2(inp)
    for _ in range(200):
        bugs = cycle2(bugs)
    print(f"Part 2: {len(bugs)}")
