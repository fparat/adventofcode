#!/usr/bin/env python3

import sys
import math


def resolve(races):
    # Searching T_H
    # t is input time, d is input distance
    # d = T_H * (t - T_H)
    # So resolve equation T_H^2 - t * T_H + d
    # and beating times are between the 2 solutions

    value = 1

    for t, d in races:
        discr = (t * t) - (4 * d)
        assert discr > 0
        th1 = (t - math.sqrt(discr)) / 2
        th2 = (t + math.sqrt(discr)) / 2

        epsilon = 0.000001
        value *= len(range(math.ceil(th1+epsilon), math.floor(th2-epsilon+1)))

    return value


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    races = list(zip(*([int(n) for n in line.split()[1:]] for line in inp.splitlines())))
    print(f"Part 1: {resolve(races)}")

    # Part 2

    races = list(zip(*([int(''.join(line.split()[1:]))] for line in inp.splitlines())))
    print(f"Part 2: {resolve(races)}")
