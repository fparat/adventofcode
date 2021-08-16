#!/usr/bin/env python3

import os
from dataclasses import dataclass
from typing import List


@dataclass
class Rule:
    name: str
    ranges: List[range]

    def validate_number(self, n):
        for rang_ in self.ranges:
            if n in rang_:
                return True
        return False


@dataclass
class Notes:
    rules: List[Rule]
    ticket: List[int]
    nearby: List[List[int]]

    @classmethod
    def from_input_file(cls, path):
        with open(path) as f:
            lines = iter(f.readlines())

        rules = []

        # Parse rules
        for line in lines:
            if not line.strip():
                break
            rule_name, constraints = line.split(":", maxsplit=1)
            txt_ranges = constraints.split("or")
            ranges = []
            for txt_range in txt_ranges:
                low, high = txt_range.split("-")
                new_range = range(int(low), int(high)+1)
                ranges.append(new_range)
            rules.append(Rule(rule_name, ranges))

        # Parse my ticket
        assert "your ticket" in next(lines)
        ticket = [int(n) for n in next(lines).split(",")]

        # Parse nearby tickets
        assert not next(lines).strip()
        assert "nearby tickets" in next(lines)
        nearby = [[int(n) for n in line.split(",")] for line in lines]

        return cls(rules, ticket, nearby)

    def find_error(self, nearby):
        for n in nearby:
            if not any(rule.validate_number(n) for rule in self.rules):
                return n
        return 0

    def validate_nearby(self, nearby):
        for n in nearby:
            if not any(rule.validate_number(n) for rule in self.rules):
                return False
        return True

    def part1(self):
        error_rate = sum(self.find_error(nearby) for nearby in self.nearby)
        print(f"Part1: error rate = {error_rate}")

    def part2(self):
        validated = [nearby for nearby in self.nearby if self.validate_nearby(nearby)] + [self.ticket]
        rule_map = {}

        for i in range(len(validated[0])):
            rules = self.rules[:]
            for rule in rules:
                if all(rule.validate_number(ticket[i]) for ticket in validated):
                    rule_map.setdefault(rule.name, []).append(i)

        rules_used = set()
        while any(len(indices) > 1 for indices in rule_map.values()):
            for indices in rule_map.values():
                if len(indices) == 1:
                    rules_used.add(indices[0])
                else:
                    for i, n in enumerate(indices):
                        if n in rules_used:
                            del indices[i]

        rule_map = {k: v[0] for k, v in rule_map.items()}

        result = 1
        for rule, index in rule_map.items():
            if rule.startswith("departure"):
                result *= self.ticket[index]
                continue

        print(f"Part2: result = {result}")


def main():
    input_file = os.path.join(os.path.dirname(__file__), "input")
    notes = Notes.from_input_file(input_file)
    notes.part1()
    notes.part2()


if __name__ == "__main__":
    main()
