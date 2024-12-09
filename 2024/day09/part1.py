#!/usr/bin/env python3

import sys
import itertools


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    disk = []
    fid = 0
    has_blk = []
    for n, c in enumerate(inp.strip()):
        if n % 2 == 0:
            has_blk += list(range(len(disk), len(disk) + int(c)))
            disk += [fid] * int(c)
            fid += 1
        else:
            disk += [None] * int(c)

    for pos, blk in enumerate(disk):
        if blk is None:
            last_blk_pos = has_blk.pop()
            if pos >= last_blk_pos:
                break
            disk[pos] = disk[last_blk_pos]
            disk[last_blk_pos] = None

    checksum = sum(pos * fid for pos, fid in enumerate(disk) if fid is not None)

    print(f"Part 1: {checksum}")
