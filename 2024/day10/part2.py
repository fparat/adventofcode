#!/usr/bin/env python3

import sys

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    grid = [[int(c) for c in line] for line in inp.splitlines()]

    starts = [(y, x) for y, line in enumerate(grid) for x, h in enumerate(line) if h == 0]

    score = 0

    for starty, startx in starts:
        visited = set()
        def dfs(y, x):
            global score
            visited.add((y, x))
            if grid[y][x] == 9:
                score += 1
                return
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = y + dy, x + dx
                if not (0 <= ny < len(grid) and 0 <= nx < len(grid[0])):
                    continue
                if (ny, nx) in visited:
                    continue
                if grid[ny][nx] != grid[y][x] + 1:
                    continue
                dfs(ny, nx)
        dfs(starty, startx)

    print(f"Part 1: {score}")

    ratings = 0
    for starty, startx in starts:
        def dfs(y, x):
            global ratings
            if grid[y][x] == 9:
                ratings += 1
                return
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = y + dy, x + dx
                if not (0 <= ny < len(grid) and 0 <= nx < len(grid[0])):
                    continue
                if grid[ny][nx] != grid[y][x] + 1:
                    continue
                dfs(ny, nx)
        dfs(starty, startx)

    print(f"Part 2: {ratings}")
