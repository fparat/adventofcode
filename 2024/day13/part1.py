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

    games = []
    presses = 0
    for game_str in inp.strip().split("\n\n"):
        game = []
        for line in game_str.splitlines():
            m = re.match(r"^.+: X.(\d+), Y.(\d+)$", line)
            game.append((int(m.group(1)), int(m.group(2))))
        games.append(tuple(game))

        # NA.XA + NB.XB = X
        # NA.YA + NB.YB = Y

        XA, YA = game[0]
        XB, YB = game[1]
        X, Y = game[2]
        Nb, Rb = divmod((X*YA - Y*XA), (XB*YA - XA*YB))
        Na, Ra = divmod((X - XB*Nb), XA)
        if Ra or Rb:
            continue
        assert Na < 100 and Nb < 100
        presses += Na * 3 + Nb

    print(f"Part 1: {presses}")
