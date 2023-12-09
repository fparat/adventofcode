#!/usr/bin/env python3

import sys
import itertools


def print_diffs(diffs):
    for n, diff in enumerate(diffs):
        print("{}{}".format("  " * n, "   ".join((str(n) for n in diff))))


def get_diffed(histories):
    diffed = []
    for seq in histories:
        diffs = [seq[:]]
        while not all(v == 0 for v in diffs[-1]):
            diffs.append([b - a for a, b in itertools.pairwise(diffs[-1])])
        diffed.append(diffs)
    return diffed


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    histories = [[int(n) for n in line.split()] for line in inp.splitlines()]
    diffed = get_diffed(histories)

    for diffs in diffed:
        diffs[-1].append(0)
        for i in range(len(diffs)-1):
            current_idx = len(diffs) - 2 - i
            prev_idx = current_idx + 1
            current = diffs[current_idx]
            predicted = current[-1] + diffs[prev_idx][-1]
            current.append(predicted)

    print(f"Part 1: {sum(d[0][-1] for d in diffed)}")

    # Part 2

    diffed = get_diffed(histories)

    for diffs in diffed:
        diffs[-1].insert(0, 0)
        for i in range(len(diffs)-1):
            current_idx = len(diffs) - 2 - i
            prev_idx = current_idx + 1
            current = diffs[current_idx]
            predicted = current[0] - diffs[prev_idx][0]
            current.insert(0, predicted)

    print(f"Part 2: {sum(d[0][0] for d in diffed)}")
