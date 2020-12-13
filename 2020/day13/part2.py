#!/usr/bin/env python3
# coding: utf-8

from collections import namedtuple


BusLine = namedtuple("BusLine", ["offset", "id"])


def part2(line):
    buses_s = [b for b in line.split(",")]
    bus_lines = [BusLine(n, int(bus)) for n, bus in enumerate(buses_s) if bus != 'x']

    # find good "period" for each bus line
    factor = 1
    base = 0
    synced_bus = set()
    while True:
        base += factor
        ok = True
        for bus_line in bus_lines:
            if (base + bus_line.offset) % bus_line.id == 0:
                if bus_line.id not in synced_bus:
                    factor *= bus_line.id
                    synced_bus.add(bus_line.id)
            else:
                ok = False
                break
        if ok:
            return base - (base % bus_lines[0].id)


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

    assert(part2("7,13,x,x,59,x,31,19") == 1068781)
    assert(part2("17,x,13,19") == 3417)
    assert(part2("67,7,59,61") == 754018)
    assert(part2("67,x,7,59,61") == 779210)
    assert(part2("67,7,x,59,61") == 1261476)
    assert(part2("1789,37,47,1889") == 1202161486)

    result = part2(lines[1])

    print(f"Part 2: {result}")


if __name__ == "__main__":
    main()
