#!/usr/bin/env python3
# coding: utf-8


def main():
    with open("input") as f:
        lines = f.read().splitlines()

    target = int(lines[0])
    buses = [int(b) for b in lines[1].split(",") if b != "x"]

    best = None
    for bus in buses:
        q = target // bus
        d = bus *  (q + 1)
        if best is None or d < best[1]:
            best = (bus, d)

    result = best[0] * (best[1] - target)

    print(f"Part 1: {result}")


if __name__ == "__main__":
    main()
