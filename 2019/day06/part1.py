#!/usr/bin/env python3
# coding: utf-8

import sys


def count_orbits(orbits, k):
    return 0 if k == "COM" else count_orbits(orbits, orbits[k]) + 1


def part1(data):
    pairs = [tuple(l.split(")")) for l  in data.splitlines()]
    orbits = { b: a for a, b in pairs }
    orbits_num = sum(count_orbits(orbits, k) for k in orbits)
    print(f"Result: {orbits_num}")


def main():
    try:
        with open(sys.argv[1]) as f:
            data = f.read()
    except IndexError:
        sys.exit("Please provide input file in argument")

    part1(data)

if __name__ == "__main__":
    main()
