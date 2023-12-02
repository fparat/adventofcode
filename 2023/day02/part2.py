#!/usr/bin/env python3

import sys

MAX_CUBES = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    games = []

    for line in inp.splitlines():
        game, sets = tuple(line.split(":", maxsplit=1))
        games.append([
            {
                color: int(ncubes)
                for ncubes, color in (cube.strip().split() for cube in set_.split(","))
            }
            for set_ in sets.split(";")
        ])

    def game_is_possible(game):
        for set_ in game:
            for color, num in set_.items():
                if num > MAX_CUBES[color]:
                    return False
        return True

    part1 = sum(n for n, game in enumerate(games, start=1) if game_is_possible(game))
    print(f"Part 1: {part1}")


    # Part 2

    part2 = 0

    for n, game in enumerate(games, start=1):
        min_cubes = { color: max(set_.get(color, 0) for set_ in game) for color in MAX_CUBES.keys() }
        part2 += min_cubes["red"] * min_cubes["green"] * min_cubes["blue"]

    print(f"Part 2: {part2}")
