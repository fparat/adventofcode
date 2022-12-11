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


class CRT:
    def __init__(self):
        self.lines = [["." for _ in range(40)] for _ in range(6)]
        self.sprite_pos = 0 # left pixel of the sprite ###
        self.pixel = 0

    def draw(self, cycle, value):
        cycle -= 1 # 0-based arithmetic
        if value - 1 <= cycle % 40 <= value + 1:
            self.lines[cycle // 40][cycle % 40] = "#"

    def print(self):
        for line in self.lines:
            print("".join(line))


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

    # Part 2

    cpu = XCPU()
    crt = CRT()

    for cycle, regx in cpu.run(program):
        crt.draw(cycle, regx)

    print("Part 2:")
    crt.print()
