#!/usr/bin/env python3

import sys
from collections import Counter

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    stones = Counter([int(s) for s in inp.split()])
    blinks = {}

    def blink(stone):
        global blinks
        try:
            return blinks[stone]
        except KeyError:
            pass

        if stone == 0:
            nstones = [1]
        elif len(str(stone)) % 2 == 0:
            stonestr = str(stone)
            split = len(stonestr) // 2
            nstones = [int(stonestr[:split]), int(stonestr[split:])]
        else:
            nstones = [stone * 2024]

        blinks[stone] = nstones
        return nstones

    for _ in range(25):
        stones2 = Counter()
        for stone in stones:
            for nstones in blink(stone):
                stones2[nstones] += stones[stone]
            stones[stone] = 0
        stones = stones2

    print(f"Part 1: {sum(stones.values())}")
