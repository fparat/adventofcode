#!/usr/bin/env python3
# coding: utf-8


def main():
    with open("input") as f:
        lines = f.read().splitlines()

    # Part 1

    trees = 0
    x = 0
    for line in lines:
        if line[x%len(line)] == "#":
            trees += 1
        x += 3

    print(f"Part1: {trees} trees")

    # Part 2

    SLOPES = [
        # (right, down)
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]

    counts = []

    for dx, dy in SLOPES:
        trees = 0
        x = 0
        for y in range(0, len(lines), dy):
            line = lines[y]
            if line[x%len(line)] == "#":
                trees += 1
            x += dx
        counts.append(trees)

    result = 1
    for count in counts:
        result *= count

    print(f"Part2: {result}")




if __name__ == "__main__":
    main()
