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


DECK_SIZE2 = 119315717514047
REPEAT_NUM = 101741582076661


# reverse
def deal_into_new_stack2(pos):
    return DECK_SIZE2 - 1 - pos


# reverse
def cut2(n, pos):
    print(f"cut {n} {pos}")
    return (pos + n) % DECK_SIZE2


def modinv(a, m):
    return pow(a, -1, m)


DECK_SIZE2 = 10
# reverse
def deal_with_increment2(n, pos):
    return modinv(n, DECK_SIZE2) * pos % DECK_SIZE2


def parse_shuffle(s: str, part2=False) -> List[Callable[[List[int]], List[int]]]:
    steps = []
    for line in s.splitlines():
        if line.startswith("deal into new stack"):
            f = deal_into_new_stack2 if part2 else deal_into_new_stack
            steps.append(f)
        elif line.startswith("cut"):
            f = cut2 if part2 else cut
            steps.append(functools.partial(f, int(line.strip().split()[-1])))
        elif line.startswith("deal with increment"):
            f = deal_with_increment2 if part2 else deal_with_increment
            steps.append(functools.partial(f, int(line.strip().split()[-1])))
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

    # Part 2, this time not mine
    # TODO understand the solution

    # https://gist.github.com/Voltara/7d417c77bc2308be4c831f1aa5a5a48d
    def github(inp):

        DECK = 119315717514047
        REPEAT = 101741582076661
        POSITION = 2020

        # The do-nothing shuffle: 0 + 1*x
        IDENTITY = [ 0, 1 ]

        # Applies shuffle f() to position x
        def shuffle_apply(f, x):
            return (f[0] + f[1] * x) % DECK

        # Takes shuffle f() and g() and returns the shuffle f(g())
        #   f(x) = a + b*x
        #   g(x) = c + d*x
        #   f(g(x)) = a + b*(c + d*x)
        #           = (a + b*c) + b*d*x
        #           = f(c) + b*d*x
        def shuffle_compose(f, g):
            return [ shuffle_apply(f, g[0]), (f[1] * g[1]) % DECK ]

        # Compose a shuffle many times with itself.
        #   repeat - how many repetitions to apply
        #   f      - the shuffle f()
        #   step   - how many repetitions f() currently represents
        def shuffle_repeat(repeat, f, step = 1):
            fN = IDENTITY
            if step <= repeat:
                fN, repeat = shuffle_repeat(repeat, shuffle_compose(f, f), step * 2)
            if step <= repeat:
                fN, repeat = shuffle_compose(f, fN), repeat - step
            return fN, repeat

        # Read the input and compose all of the shuffle steps
        shuf = IDENTITY
        for line in [ s.strip() for s in inp.splitlines() ]:
            f = line.split()
            if line == "deal into new stack":
                shuf = shuffle_compose([ -1, -1 ], shuf)
            elif line.startswith("cut"):
                shuf = shuffle_compose([ -int(f[1]), 1 ], shuf)
            elif line.startswith("deal with increment"):
                shuf = shuffle_compose([ 0, int(f[3]) ], shuf)

        # Observation: Repeating the shuffle (DECK - 1) times returns it to
        # the original ordering.  While this does not necessarily hold true
        # for all deck sizes, it works for the deck size given in Part 2.
        # (Experiment idea: What deck sizes does it work for?)
        assert(shuffle_repeat(DECK - 1, shuf)[0] == IDENTITY)

        # This gives us a way to apply the shuffle in reverse.  If we repeat
        # the shuffle (DECK - 1 - n) times, it brings the deck to a state where
        # n more shuffles will restore it to factory order.  This is exactly
        # the same as reversing the shuffle n times.
        shufN, _ = shuffle_repeat(DECK - 1 - REPEAT, shuf)
        return shuffle_apply(shufN, POSITION)

    print(f"Part 2: {github(inp)}")

    # # reverse steps of position 2020
    # steps = parse_shuffle(inp, part2=True)
    # pos = 2020
    # for step in reversed(steps):
    #     pos = step(pos)
    #     print(pos)
