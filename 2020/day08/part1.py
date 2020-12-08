#!/usr/bin/env python3
# coding: utf-8

from collections import namedtuple

OP_ACC = "acc"
OP_JMP = "jmp"
OP_NOP = "nop"

Instruction = namedtuple("Instruction", ["op", "arg"])

class Code:
    def __init__(self, instructions):
        self.instructions = list(instructions)

    @classmethod
    def parse(cls, s):
        instructions = [Instruction(x[0], int(x[1])) for x in map(str.split, s.splitlines())]
        return cls(instructions)

    def __getitem__(self, i):
        return self.instructions[i]

class Breakpoint(Exception):
    pass

class Machine:
    def __init__(self, code):
        self.code = code
        self.pc = 0  # program counter
        self.acc = 0  # accumulator value
        self.trace = set()

        self.debug = False
        self.break_on_rerun = False

    @classmethod
    def parse_new(cls, s):
        return cls(Code.parse(s))

    def __repr__(self):
        return f"Machine<pc={self.pc}, acc={self.acc}> : {repr(self.code[self.pc])}"

    def _print(self, *args, **kwargs):
        if self.debug:
            print(*args, flush=True, **kwargs)

    def step(self):
        if self.break_on_rerun and self.pc in self.trace:
            self._print(f"Breakpoint: {self}")
            raise Breakpoint(self)
        self.trace.add(self.pc)
        instruction = self.code[self.pc]
        self._print(f"exec {instruction} @ {self.pc}, acc={self.acc}")
        {
            OP_ACC: self._acc,
            OP_JMP: self._jmp,
            OP_NOP: self._nop,
        }[instruction.op](instruction.arg)
        self.pc += 1

    def _acc(self, arg):
        self.acc += arg

    def _jmp(self, arg):
        self.pc += arg - 1 # anticipate incrementation of PC

    def _nop(self, arg):
        pass

    def run(self):
        while True:
            self.step()


def main():
    with open("input") as f:
        machine = Machine.parse_new(f.read())

    # Uncomment to print trace
    #machine.debug = True

    machine.break_on_rerun = True
    try:
        machine.run()
    except Breakpoint:
        print(f"Part 1: {machine.acc}")


if __name__ == "__main__":
    main()
