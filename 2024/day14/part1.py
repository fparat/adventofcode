#!/usr/bin/env python3

import sys

W = 101
H = 103

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    if filename == "example":
        W = 11
        H = 7

    robots = []
    for line in inp.splitlines():
        p, v = line.split()
        _, p = p.split('=')
        px, py =  p.split(',')
        _, v = v.split('=')
        vx, vy = v.split(',')
        robots.append(((int(px), int(py)), (int(vx), int(vy))))

    def simulate(step_num):
        robots_end = []
        for robot in robots:
            (px, py), (vx, vy) = robot
            pxe = (px + (vx * step_num)) % W
            pye = (py + (vy * step_num)) % H
            robots_end.append((pxe, pye))
        return robots_end

    def calc_safety(robots):
        nw = sum(r[0] < (W//2) and r[1] < (H//2) for r in robots)
        ne = sum(r[0] > (W//2) and r[1] < (H//2) for r in robots)
        se = sum(r[0] > (W//2) and r[1] > (H//2) for r in robots)
        sw = sum(r[0] < (W//2) and r[1] > (H//2) for r in robots)
        return nw * ne * se * sw

    robots100 = simulate(100)
    safety = calc_safety(robots100)

    print(f"Part 1: {safety}")
