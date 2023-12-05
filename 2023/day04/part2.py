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

    def win_num(line):
        winning, have = [set(int(n) for n in g.split()) for g in line.split(':')[1].split('|')]
        return len(winning.intersection(have))

    part1 = 0
    for line in inp.splitlines():
        if (num := win_num(line)) > 0:
            part1 += 1 << (num - 1)

    print(f"Part 1: {part1}")

    # Part 2

    lines = inp.splitlines()
    total = []
    copies = []
    for card, line in enumerate(lines, start=1):
        total.append(card)
        copies += range(card+1, card+1+win_num(line))
    while copies:
        card = copies.pop()
        line = lines[card-1]
        total.append(card)
        copies += range(card+1, card+1+win_num(line))

    print(f"Part 2: {len(total)}")
