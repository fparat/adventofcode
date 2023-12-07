#!/usr/bin/env python3

import sys

# Hand types by strength
FIVE_KIND = 7
FOUR_KIND = 6
FULL_HOUSE = 5
THREE_KIND = 4
TWO_PAIR = 3
ONE_PAIR = 2
HIGH_CARD = 1

STRENGTH = {
    "2":  2,
    "3":  3,
    "4":  4,
    "5":  5,
    "6":  6,
    "7":  7,
    "8":  8,
    "9":  9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


class Hand:
    def __init__(self, hand, bid):
        self.type = Hand.find_type(hand)
        self.hand = str(hand)
        self.bid = int(bid)

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type}, hand={self.hand}, bid={self.bid})"

    def cmp_key(self):
        return (self.type, *[STRENGTH[c] for c in self.hand])

    @staticmethod
    def find_type(hand: str):
        s = set(hand)
        if len(s) == 5:
            return HIGH_CARD
        elif len(s) == 4:
            return ONE_PAIR
        elif len(s) == 3:
            if all(hand.count(c) <= 2 for c in hand):
                return TWO_PAIR
            elif any(hand.count(c) == 3 for c in hand):
                return THREE_KIND
        elif len(s) == 2:
            if hand.count(hand[0]) in [2, 3]:
                return FULL_HOUSE
            elif hand.count(hand[0]) in [1, 4]:
                return FOUR_KIND
        elif len(s) == 1:
            return FIVE_KIND
        assert False, f"{hand=}"


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    hands = sorted((Hand(*line.split()) for line in inp.splitlines()), key=lambda hand:hand.cmp_key())
    result = sum(hand.bid * rank for rank, hand in enumerate(hands, start=1))
    print(f"Part 1: {result}")
