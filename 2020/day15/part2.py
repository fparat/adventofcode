#!/usr/bin/env python3
# coding: utf-8

import os
import itertools


def take(iterable, n):
    "Return first n items of the iterable as a list"
    return list(itertools.islice(iterable, n))


def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    return next(itertools.islice(iterable, n, None), default)


def memory_game(starts):
    spoken = {}

    # Read starting numbers
    for turn, n in enumerate(starts):
        try:
            last, previous = spoken[n]
            spoken[n] = (turn, last)
        except KeyError:
            spoken[n] = (turn, turn)
            last = turn
        yield n

    # Play
    for turn in itertools.count(len(starts)):
        try:
            last, previous = spoken[n]
            x = last - previous
        except KeyError:
            x = 0
            last = turn
        last_x = spoken.get(x, (turn, 0))[0]
        spoken[x] = (turn, last_x)
        yield x
        n = x


def play_get(starts, target):
    return nth(memory_game(starts), target-1)


def main():
    input_file = os.path.join(os.path.dirname(__file__), "input")
    with open(input_file) as f:
        starts = [int(n) for n in f.read().split(",")]

    assert(take(memory_game([0, 3, 6]), 10) == [0, 3, 6, 0, 3, 3, 1, 0, 4, 0])
    assert(play_get([0, 3, 6], 2020) == 436)
    assert(play_get([1,3,2], 2020) == 1)
    assert(play_get([2,1,3], 2020) == 10)
    assert(play_get([1,2,3], 2020) == 27)
    assert(play_get([2,3,1], 2020) == 78)
    assert(play_get([3,2,1], 2020) == 438)
    assert(play_get([3,1,2], 2020) == 1836)

    part1 = play_get(starts, 2020)
    print(f"Part 1: {part1}")

    part2 = play_get(starts, 30000000)
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
