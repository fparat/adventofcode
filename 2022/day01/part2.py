import sys

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1
    calories = [sum(int(line.strip()) for line in elf.splitlines()) for elf in inp.split("\n\n")]
    print(f"Part 1: {max(calories)}")

    # Part 2
    top3 = sorted(calories, reverse=True)[:3]
    print(f"Part 2: {sum(top3)}")
