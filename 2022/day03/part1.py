import sys
import string

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1
    priorities = " " + string.ascii_lowercase + string.ascii_uppercase
    total_prio = 0

    for line in inp.splitlines():
        half = len(line) // 2
        first = line[:half]
        second = line[half:]
        assert len(first) == len(second) == half

        common = set(first).intersection(set(second))
        assert len(common) == 1

        item = common.pop()
        item_prio = priorities.find(item)
        total_prio += item_prio

    print(f"Part 1: {total_prio}")
