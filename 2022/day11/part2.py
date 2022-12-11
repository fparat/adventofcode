#!/usr/bin/env python3

import sys


class Monkey:
    def __init__(self, idx, items, operation, test_val, test_true, test_false):
        self.idx = int(idx)
        self.items = list(items)
        self.operation = operation
        self.test_val = int(test_val)
        self.test_true = int(test_true)
        self.test_false = int(test_false)

        self.inspected = 0

    def __repr__(self):
        return f"Monkey(idx={self.idx}, items={self.items}, operation=func, test_val={self.test_val}, test_true={self.test_true}, test_false={self.test_false})"

    @classmethod
    def from_str(cls, s):
        lines = s.splitlines()

        idx = int(lines[0].split()[1][:-1])

        items = map(int, lines[1].split(":")[1].split(","))

        optoks = lines[2].split()
        if optoks[-1] == "old":
            operation = {
                "+": lambda old: old + old,
                "*": lambda old: old * old,
            }[optoks[-2]]
        else:
            opval = int(optoks[-1])
            operation = {
                "+": lambda old: old + opval,
                "*": lambda old: old * opval,
            }[optoks[-2]]

        test_val = int(lines[3].split()[-1])
        test_true = int(lines[4].split()[-1])
        test_false = int(lines[5].split()[-1])

        return cls(idx, items, operation, test_val, test_true, test_false)

    def inspect_item(self):
        try:
            worry = self.items.pop(0)
        except IndexError:
            return None

        worry = self.operation(worry)
        worry //= 3

        self.inspected += 1

        if worry % self.test_val == 0:
            return self.test_true, worry
        else:
            return self.test_false, worry

    def inspect_item_no_relief(self, multiple):
        try:
            worry = self.items.pop(0)
        except IndexError:
            return None

        worry = self.operation(worry) % multiple

        self.inspected += 1

        # primes = prime_factors(worry)

        # if worry in primes == 0:
        if worry % self.test_val == 0:
            return self.test_true, worry
        else:
            return self.test_false, worry


def prime_factors(n):
    i = 2
    primes = set()
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            primes.add(i)
    if n > 1:
        primes.add(n)
    return primes


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    monkeys = [Monkey.from_str(s) for s in inp.split("\n\n")]

    for round in range(20):
        for monkey in monkeys:
            while monkey.items:
                dest, item = monkey.inspect_item()
                monkeys[dest].items.append(item)

    inspections = sorted(monkey.inspected for monkey in monkeys)
    monkey_business = inspections[-1] * inspections[-2]
    print(f"Part 1: {monkey_business}")

    # Part 2

    monkeys = [Monkey.from_str(s) for s in inp.split("\n\n")]

    # we will modulo the worry level with the common multiple of test vals
    multiple = 1
    for monkey in monkeys:
        multiple *= monkey.test_val

    for round in range(10000):
        for monkey in monkeys:
            while monkey.items:
                dest, item = monkey.inspect_item_no_relief(multiple)
                monkeys[dest].items.append(item)

    inspections = sorted(monkey.inspected for monkey in monkeys)
    monkey_business = inspections[-1] * inspections[-2]
    print(f"Part 2: {monkey_business}")
