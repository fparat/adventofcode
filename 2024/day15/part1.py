#!/usr/bin/env python3

import sys


ROBOT = '@'
BOX = 'O'
WALL = '#'
EMPTY = '.'

N = "^"
E = ">"
S = "v"
W = "<"

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    grid, moves = inp.split("\n\n")

    grid = [list(line) for line in grid.splitlines()]
    moves = [c for c in moves if c in N+E+S+W]

    def find_robot(grid):
        for y, line in enumerate(grid):
            for x, c in enumerate(line):
                if c == ROBOT:
                    return y, x

    robot = find_robot(grid)

    def draw(grid):
        for line in grid:
            for c in line:
                print(c, end="")
            print()
        print()

    def step(pos, dir):
        y, x = pos
        dy, dx = dir
        ny, nx = y+dy, x+dx

        if grid[ny][nx] == WALL:
            return y, x

        if grid[ny][nx] == BOX:
            step((ny, nx), dir)

        if grid[ny][nx] == EMPTY:
            grid[ny][nx] = grid[y][x]
            grid[y][x] = EMPTY
            return ny, nx

        return y, x

    for n, move in enumerate(moves):
        dy, dx = { N: (-1, 0), E: (0, 1), S: (1, 0), W: (0, -1) }[move]
        robot = step(robot, (dy, dx))
        # print(n)
        # draw(grid)

    part1 = sum(100 * y + x for y, line in enumerate(grid) for x, c in enumerate(line) if c == BOX)

    print(f"Part 1: {part1}")
