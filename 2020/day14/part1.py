#!/usr/bin/env python3
# coding: utf-8

import re


class Machine:
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



def main():
    with open("input") as f:
        s = f.read()

    machine = Machine(s.splitlines())
    machine.run()
    result = sum(machine.memory.values())
    print(f"Part 1: {result}")




if __name__ == "__main__":
    main()
