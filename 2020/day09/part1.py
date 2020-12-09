#!/usr/bin/env python3
# coding: utf-8

import itertools


def find_bad_num(nums, preamble_len):
    for i in range(preamble_len, len(nums)):
        previous, num = nums[i-preamble_len:i], nums[i]
        ok = any((a+b) == num for a, b in itertools.permutations(previous, 2))
        if not ok:
            return num


def main():
    with open("input") as f:
        nums = [int(l) for l in f]

    print("Part 1: ", find_bad_num(nums, 25))


if __name__ == "__main__":
    main()
