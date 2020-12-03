#!/usr/bin/env python3
# coding: utf-8


def main():
    with open("input") as f:
        lines = f.read().splitlines()

    trees = 0
    x = 0
    for line in lines:
        if line[x%len(line)] == "#":
            trees += 1
        x += 3

    print(f"Part1: {trees} trees")


if __name__ == "__main__":
    main()
