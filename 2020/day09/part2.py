#!/usr/bin/env python3
# coding: utf-8

import itertools


def find_bad_num(nums, preamble_len):
    for i in range(preamble_len, len(nums)):
        previous, num = nums[i-preamble_len:i], nums[i]
        ok = any((a+b) == num for a, b in itertools.permutations(previous, 2))
        if not ok:
            return num


def find_weakness(nums, preamble_len):
    invalid = find_bad_num(nums, preamble_len)
    for i in range(len(nums)):
        for j in range(i+2, len(nums)):
            seq = nums[i:j]
            if sum(seq) == invalid:
                return max(seq) + min(seq)


def main():
    with open("input") as f:
        nums = [int(l) for l in f]
    print("Part 1: ", find_bad_num(nums, 25))
    print("Part 2:", find_weakness(nums, 25))



if __name__ == "__main__":
    main()
