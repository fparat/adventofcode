#!/usr/bin/env python3
# coding: utf-8


def main():
    with open("input") as f:
        ratings = [int(l) for l in f.read().splitlines()]

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

    print(f"Part 1: {diffs[1] * diffs[3]}")


if __name__ == "__main__":
    main()
