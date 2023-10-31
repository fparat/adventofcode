#!/usr/bin/env python3

import sys
import functools
from typing import *


def deal_into_new_stack(deck):
    return list(reversed(deck))


def cut(n, deck):
    return deck[n:] + deck[:n]


def deal_with_increment(n, deck):
    new_deck = [0 for _ in range(len(deck))]
    pos = 0
    for i, card in enumerate(deck):
        new_deck[pos] = card
        pos = (pos + n) % len(deck)
    return new_deck


def parse_shuffle(s: str) -> List[Callable[[List[int]], List[int]]]:
    steps = []
    for line in s.splitlines():
        if line.startswith("deal into new stack"):
            steps.append(deal_into_new_stack)
        elif line.startswith("cut"):
            steps.append(functools.partial(cut, int(line.strip().split()[-1])))
        elif line.startswith("deal with increment"):
            steps.append(functools.partial(deal_with_increment, int(line.strip().split()[-1])))
    return steps


def new_deck(size=10007) -> List[int]:
    return list(range(size))


def test_example(example: str):
    expected = [int(n) for n in example.splitlines()[-1].split(maxsplit=1)[-1].split()]
    deck = new_deck(10)
    for step in parse_shuffle(example):
        deck = step(deck)
        # print(deck)
    assert deck == expected, f"expected {expected}"


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    test_example("""\
deal with increment 7
deal into new stack
deal into new stack
Result: 0 3 6 9 2 5 8 1 4 7
""")

    test_example("""\
cut 6
deal with increment 7
deal into new stack
Result: 3 0 7 4 1 8 5 2 9 6
""")

    test_example("""\
deal with increment 7
deal with increment 9
cut -2
Result: 6 3 0 7 4 1 8 5 2 9
""")

    test_example("""\
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
Result: 9 2 5 8 1 4 7 0 3 6
""")

    # Part 1

    deck = new_deck()
    for step in parse_shuffle(inp):
        deck = step(deck)

    print(f"Part 1: {deck.index(2019)}")
