#!/usr/bin/env python3

import sys


ROBOT = '@'
BOX = 'O'
WBOXL = '['
WBOXR = ']'
WBOX = WBOXL + WBOXR
WALL = '#'
EMPTY = '.'

N = "^"
E = ">"
S = "v"
W = "<"

DIRS = {
    N: (-1, 0),
    E: (0, 1),
    S: (1, 0),
    W: (0, -1)
}


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
        print("   ", end="")
        for x in range(len(grid[0])):
            print(x%10, end="")
        print()
        for y, line in enumerate(grid):
            print(f"{y:>02} ", end="")
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
        dy, dx = DIRS[move]
        robot = step(robot, (dy, dx))
        # print(n)
        # draw(grid)

    part1 = sum(100 * y + x for y, line in enumerate(grid) for x, c in enumerate(line) if c == BOX)

    print(f"Part 1: {part1}")

    # Part2

    grid, moves = inp.split("\n\n")

    grid = [list(line) for line in grid.splitlines()]
    moves = [c for c in moves if c in N+E+S+W]

    def wide_grid(grid):
        wgrid = []
        for line in grid:
            wline = []
            for c in line:
                if c == ROBOT:
                    wline.extend(ROBOT+EMPTY)
                elif c == BOX:
                    wline.extend(WBOX)
                elif c == WALL:
                    wline.extend(2*WALL)
                elif c == EMPTY:
                    wline.extend(2*EMPTY)
            wgrid.append(wline)
        return wgrid

    grid = wide_grid(grid)
    robot = find_robot(grid)

    def move_cell(pos, dir):
        y, x = pos
        dy, dx = dir
        ny, nx = y+dy, x+dx
        assert grid[ny][nx] == EMPTY
        grid[ny][nx] = grid[y][x]
        grid[y][x] = EMPTY
        return ny, nx

    def robot_step(pos, dir):
        y, x = pos
        dy, dx = dir
        ny, nx = y+dy, x+dx

        def is_vertical(dir):
            return dir in [DIRS[N], DIRS[S]]

        def is_collision(y, x):
            dy, dx = dir
            if grid[y][x] == WBOXL:
                return is_collision(y+dy, x+dx) or (is_vertical(dir) and is_collision(y+dy, x+dx+1))
            elif grid[y][x] == WBOXR:
                return is_collision(y+dy, x+dx) or (is_vertical(dir) and is_collision(y+dy, x+dx-1))
            elif grid[y][x] == WALL:
                return True
            elif grid[y][x] == EMPTY:
                return False
            raise "unreachable"

        def move_box(y, x):
            dy, dx = dir
            ny, nx = y+dy, x+dx
            assert grid[y][x] in WBOX
            if grid[y][x] == WBOXL:
                if grid[ny][nx] in WBOX:
                    move_box(ny, nx)
                if is_vertical(dir):
                    if grid[ny][nx+1] in WBOX:
                        move_box(ny, nx+1)
                    move_cell((y, x+1), dir)
                move_cell((y, x), dir)
            elif grid[y][x] == WBOXR:
                if grid[ny][nx] in WBOX:
                    move_box(ny, nx)
                if is_vertical(dir):
                    if grid[ny][nx-1] in WBOX:
                        move_box(ny, nx-1)
                    move_cell((y, x-1), dir)
                move_cell((y, x), dir)

        if is_collision(ny, nx):
            return y, x

        if grid[ny][nx] in WBOX:
            move_box(ny, nx)

        if grid[ny][nx] == EMPTY:
            return move_cell(pos, dir)

        raise "unreachable"


    for n, move in enumerate(moves, 1):
        dy, dx = DIRS[move]
        robot = robot_step(robot, (dy, dx))
        # print(n)
        # draw(grid)

    part2 = sum(100 * y + x for y, line in enumerate(grid) for x, c in enumerate(line) if c == WBOXL)

    print(f"Part 2: {part2}")
