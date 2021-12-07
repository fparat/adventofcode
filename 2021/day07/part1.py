#!/usr/bin/env python3

import sys

def part1(crabs):
	result = 999999999999
	for n in range(min(crabs), max(crabs) + 1):
		fuel = sum(abs(crab - n) for crab in crabs)
		if fuel < result:
			result = fuel
	print(f"Part 1: {result}")


if __name__ == "__main__":
	try:
		filename = sys.argv[1]
	except IndexError:
		filename = "input"

	with open(filename) as f:
		crabs = [int(i) for i in f.read().split(',')]

	part1(crabs[:])
