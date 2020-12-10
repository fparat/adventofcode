#!/usr/bin/env python3
# coding: utf-8


def part1(ratings):

    builtin = max(ratings) + 3
    ratings.append(builtin)

    diffs = {}
    diff = 0
    for j in range(builtin + 1):
        if j in ratings:
            diffs[diff] = diffs.get(diff, 0) + 1
            diff = 1
        else:
            diff += 1
    return diffs[1] * diffs[3]


def part2(ratings):
    deltas = []
    rp = 0
    for r in sorted(ratings):
        deltas.append(r - rp)
        rp = r

    # isolate "groups" of +1 jolts, they are separated by +3 jolts
    groups = ''.join(str(d) for d in deltas)
    groups = [len(g) - 1 for g in groups.split("3") if g]

    combinations = 1
    for g in groups:
        factor = 2 ** g
        # for groups with than three +1 jolt we need to ignore combinations with +4 jolts or more
        if g >= 3:
            factor -= 2 ** (g % 3)  # good formula? the input doesn't exceed 3
        combinations *= factor

    return combinations


def main():
    with open("input") as f:
        ratings = [int(l) for l in f.read().splitlines()]

    print(f"Part 1: {part1(ratings)}")
    print(f"Part 2: {part2(ratings)}")


if __name__ == "__main__":
    main()
