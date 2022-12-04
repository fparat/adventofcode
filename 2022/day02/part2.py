import sys

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1
    rounds = inp.splitlines()
    scores = [{
        "A X": 1 + 3,
        "A Y": 2 + 6,
        "A Z": 3 + 0,
        "B X": 1 + 0,
        "B Y": 2 + 3,
        "B Z": 3 + 6,
        "C X": 1 + 6,
        "C Y": 2 + 0,
        "C Z": 3 + 3,
    }[round] for round in rounds]
    print(f"Part1: {sum(scores)}")

    # Part 2
    R = 1
    P = 2
    S = 3
    L = 0
    D = 3
    W = 6
    scores = [{
        "A X": L + S,
        "A Y": D + R,
        "A Z": W + P,
        "B X": L + R,
        "B Y": D + P,
        "B Z": W + S,
        "C X": L + P,
        "C Y": D + S,
        "C Z": W + R,
    }[round] for round in rounds]
    print(f"Part2: {sum(scores)}")
