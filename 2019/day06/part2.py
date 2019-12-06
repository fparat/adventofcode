#!/usr/bin/env python3
# coding: utf-8

import sys
import itertools


def count_orbits(orbits, k):
    return 0 if k == "COM" else count_orbits(orbits, orbits[k]) + 1


def part1(data):
    pairs = [tuple(l.split(")")) for l  in data.splitlines()]
    orbits = { b: a for a, b in pairs }
    orbits_num = sum(count_orbits(orbits, k) for k in orbits)
    print(f"Result: {orbits_num}")


def part2(data):
    pairs = [tuple(l.split(")")) for l  in data.splitlines()]
    orbits = { b: a for a, b in pairs }

    def path_from_com(k):
        path = []
        while k != "COM":
            n = orbits[k]
            path.append(n)
            k = n
        return list(reversed(path))

    you_path = path_from_com("YOU")
    san_path = path_from_com("SAN")

    branches = zip(*itertools.dropwhile(
        lambda x: x[0] == x[1],
        itertools.zip_longest(you_path, san_path, fillvalue=None)))

    print(f"Result: {sum(sum(1 for _ in filter(None, x)) for x in branches)}")


def main():
    try:
        with open(sys.argv[1]) as f:
            data = f.read()
    except IndexError:
        sys.exit("Please provide input file in argument")

    part2(data)

if __name__ == "__main__":
    main()
