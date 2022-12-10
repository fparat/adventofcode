import sys

def print_visibles(visibles, x, y):
    for r in range(x):
        for c in range(y):
            if (r, c) in visibles:
                print("o", end="")
            else:
                print(".", end="")
        print()
    print()

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    trees = [list(map(int, line)) for line in inp.splitlines()]

    # count borders
    visibles = set()
    for r in range(len(trees)):
        visibles.add((r, 0))
        visibles.add((r, len(trees[0]) - 1))
    for c in range(len(trees[0])):
        visibles.add((0, c))
        visibles.add((len(trees) - 1, c))

    # view from top and bottom
    for c in range(1, len(trees[0]) - 1):
        h = trees[0][c]
        for r in range(1, len(trees) - 1):
            if trees[r][c] > h:
                visibles.add((r, c))
                h = trees[r][c]

        h = trees[-1][c]
        for r in range(-2, -len(trees), -1):
            if trees[r][c] > h:
                visibles.add((r + len(trees), c))
                h = trees[r][c]

    # view from left and right
    for r in range(1, len(trees) - 1):
        h = trees[r][0]
        for c in range(1, len(trees[0]) - 1):
            if trees[r][c] > h:
                visibles.add((r, c))
                h = trees[r][c]

        h = trees[r][-1]
        for c in range(-2, -len(trees[0]), -1):
            newh = trees[r][c]
            if trees[r][c] > h:
                visibles.add((r, len(trees[0]) + c))
                h = trees[r][c]

    print_visibles(visibles, len(trees[0]), len(trees))

    print(f"Part 1: {len(visibles)}")

    # Part 2

    scores = {}
    for r in range(len(trees)):
        for c in range(len(trees[0])):
            h = trees[r][c]
            score = 1

            dr = 1
            count = 0
            while r + dr < len(trees):
                count += 1
                if trees[r+dr][c] >= h:
                    break
                dr += 1
            if count > 0:
                score *= count

            dr = -1
            count = 0
            while r + dr >= 0:
                count += 1
                if trees[r+dr][c] >= h:
                    break
                dr -= 1
            if count > 0:
                score *= count

            dc = 1
            count = 0
            while c + dc < len(trees[0]):
                count += 1
                if trees[r][c+dc] >= h:
                    break
                dc += 1
            if count > 0:
                score *= count

            dc = -1
            count = 0
            while c + dc >= 0:
                count += 1
                if trees[r][c+dc] >= h:
                    break
                dc -= 1
            if count > 0:
                score *= count

            scores[(r, c)] = score

    print(f"Part 2: {max(scores.values())}")
