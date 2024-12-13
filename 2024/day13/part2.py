#!/usr/bin/env python3

import sys
import re

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    def solve(game):
        # NA.XA + NB.XB = X
        # NA.YA + NB.YB = Y
        XA, YA = game[0]
        XB, YB = game[1]
        X, Y = game[2]
        Nb, Rb = divmod((X * YA - Y * XA), (XB * YA - XA * YB))
        Na, Ra = divmod((X - XB * Nb), XA)
        if Ra or Rb:
            return 0
        return Na * 3 + Nb

    games = []
    presses = 0
    for game_str in inp.strip().split("\n\n"):
        game = []
        for line in game_str.splitlines():
            m = re.match(r"^.+: X.(\d+), Y.(\d+)$", line)
            game.append((int(m.group(1)), int(m.group(2))))
        games.append(tuple(game))
        presses += solve(game)

    print(f"Part 1: {presses}")

    presses = 0
    D = 10000000000000
    for game in games:
        game = (game[0], game[1], (game[2][0] + D, game[2][1] + D))
        presses += solve(game)

    print(f"Part 2: {presses}")
