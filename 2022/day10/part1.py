#!/usr/bin/env python3

import sys


class XCPU:
    def __init__(self):
        self.regx = 1
        self.cycle = 0
        self.pipeline = [0, 0]

    def run(self, program):
        for instr in program:
            tok = instr.split()
            if tok[0] == "noop":
                self.cycle += 1
                yield self.cycle, self.regx
            elif tok[0] == "addx":
                self.cycle += 1
                yield self.cycle, self.regx
                self.cycle += 1
                yield self.cycle, self.regx
                self.regx += int(tok[1])


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    cpu = XCPU()
    program = inp.splitlines()
    signal = 0

    for cycle, regx in cpu.run(program):
        if cycle in [20, 60, 100, 140, 180, 220]:
            signal += cycle * regx

    print(f"Part 1: {signal}")
