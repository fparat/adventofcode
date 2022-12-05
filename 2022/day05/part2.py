import sys

def draw(stacks):
    stacks = [stack[:] for stack in stacks]
    max_len = max(len(stack) for stack in stacks)
    lines = ["".join(f" {i+1}  " for i in range(len(stacks)))]
    for i in range(max_len):
        crates = []
        for stack in stacks:
            try:
                crate = f"[{stack.pop(0)}] "
            except IndexError:
                crate = "    "
            crates.append(crate)
        line = "".join(crates)
        lines.append(line)

    for line in reversed(lines):
        print(line)


def parse_stacks(stacks_draw):
    stacks_lines = stacks_draw.splitlines()
    stack_num = len(stacks_lines.pop().split())
    stacks = [[] for _ in range(stack_num)]
    for line in reversed(stacks_lines):
        for i in range(stack_num):
            # [L] [C] [W]
            # 0123456789
            pos = 4 * i + 1
            crate = line[pos]
            if crate.strip():
                stacks[i].append(crate)

    return stacks


def parse_instructions(procedure):
    instructions = []
    for line in procedure.splitlines():
        # move 2 from 5 to 9
        toks = line.split()
        num = int(toks[1])
        start = int(toks[3]) - 1
        end = int(toks[5]) - 1
        instructions.append((num, start, end))

    return instructions


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1
    stacks_draw, procedure = inp.split("\n\n")
    stacks = parse_stacks(stacks_draw)
    instructions = parse_instructions(procedure)

    draw(stacks)
    for num, start, end in instructions:
        print(f"move {num} from {start} to {end}")
        for i in range(num):
            crate = stacks[start].pop()
            stacks[end].append(crate)
        draw(stacks)

    tops = "".join([stack[-1] for stack in stacks])
    print(f"Part 1: {tops}")

    # Part 2
    stacks = parse_stacks(stacks_draw)
    draw(stacks)
    for num, start, end in instructions:
        print(f"move {num} from {start} to {end}")
        crates = stacks[start][-num:]
        del stacks[start][-num:]
        stacks[end] += crates
        draw(stacks)

    tops = "".join([stack[-1] for stack in stacks])
    print(f"Part 2: {tops}")
