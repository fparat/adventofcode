import sys

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1
    assignments = []
    for pair_assigment in inp.splitlines():
        ranges = [list(map(int, range_.split("-"))) for range_ in pair_assigment.split(",")]
        assignments.append(ranges)

    contained = 0
    for first, second in assignments:
        contained += int((first[0] >= second[0] and first[1] <= second[1]) or (first[0] <= second[0] and first[1] >= second[1]))

    print(f"Part 1: {contained}")

    # Part 2
    overlap = 0
    for first, second in assignments:
        overlap += int((first[0] >= second[1] and first[1] <= second[0]) or (first[0] <= second[1] and first[1] >= second[0]))
    print(f"Part 2: {overlap}")
