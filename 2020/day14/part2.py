#!/usr/bin/env python3
# coding: utf-8

import re


class MachineV1:
    def __init__(self, instructions):
        self.instructions = instructions
        self.mask = 'X'
        self.memory = {}

    def apply_mask(self, value):
        mask = int(self.mask.replace('0', '1').replace('X', '0'), 2)
        overwrite = int(self.mask.replace('X', '0'), 2)
        return (overwrite & mask) | (value & (~mask))

    def run(self):
        for instruction in self.instructions:
            m = re.match(r"mask = ([01X]+)", instruction)
            if m:
                self.mask = m.group(1)
                continue
            m = re.match(r"mem\[(\d+)\] = (\d+)", instruction)
            if m:
                address = int(m.group(1))
                value = int(m.group(2))
                value_set = self.apply_mask(value)
                self.memory[address] = value_set


class MachineV2:
    def __init__(self, instructions):
        self.instructions = instructions
        self.mask = 'X'
        self.memory = {}

    def find_addresses(self, address):
        floating_positions = [n for n, b in enumerate(reversed(self.mask)) if b == 'X']
        addresses = []
        bitmask = int(self.mask.replace('X', '0'), 2)
        floatmask = int(self.mask.replace('0', '1').replace('X', '0'), 2)
        for combination in range(1 << len(floating_positions)):
            floating_bits = 0
            for n, pos in enumerate(floating_positions):
                floating_bits |= ((combination >> n) & 1) << pos
            a = ((address| bitmask) & floatmask) | floating_bits
            addresses.append(a)
        return addresses

    def run(self):
        for instruction in self.instructions:
            m = re.match(r"mask = ([01X]+)", instruction)
            if m:
                self.mask = m.group(1)
                continue
            m = re.match(r"mem\[(\d+)\] = (\d+)", instruction)
            if m:
                address = int(m.group(1))
                value = int(m.group(2))
                addresses = self.find_addresses(address)
                for address in addresses:
                    self.memory[address] = value


def main():
    with open("input") as f:
        s = f.read()

    machine = MachineV1(s.splitlines())
    machine.run()
    result = sum(machine.memory.values())
    print(f"Part 1: {result}")

    machine2 = MachineV2(s.splitlines())
    machine2.run()
    result = sum(machine2.memory.values())
    print(f"Part 2: {result}")


if __name__ == "__main__":
    main()
