#!/usr/bin/env python3
# coding: utf-8

import itertools

if __name__ == "__main__":
    for seq in itertools.permutations(range(5, 10)):
        print("    {{ {} }},".format(", ".join(map(str, seq))))
