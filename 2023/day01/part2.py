#!/usr/bin/env python3

import sys


def part1(lines):
    return sum(map(lambda c:int(c[0]+c[-1]),map(lambda l:list(filter(str.isdigit,l)),lines)))


DIGITS = {
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "one":   "1",
    "two":   "2",
    "three": "3",
    "four":  "4",
    "five":  "5",
    "six":   "6",
    "seven": "7",
    "eight": "8",
    "nine":  "9",
}


def part2(lines):
    total = 0

    for line in lines:
        found, first = None, None
        for k, v in DIGITS.items():
            idx = line.find(k)
            if idx >= 0 and (found is None or idx < found):
                found, first = idx, v

        found, last = None, None
        for k, v in DIGITS.items():
            idx = line.rfind(k)
            if idx >= 0 and (found is None or idx > found):
                found, last = idx, v

        total += int(first+last)

    return total


if __name__ == "__main__":
    lines = list(sys.stdin)
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
