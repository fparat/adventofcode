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

    for step_num in range(10000):
        robots_step = set(simulate(step_num))

        # heuristic: check when mean of coordinates are too biased from center
        meanx = sum(r[0] for r in robots_step) / len(robots_step) / W
        meany = sum(r[1] for r in robots_step) / len(robots_step) / H

        e = 0.06
        if abs(meanx - 0.5) < e or abs(meany - 0.5) < e:
            continue

        print("⎯" * W)
        print(f"\n[{step_num}]")
        for y in range(H):
            for x in range(W):
                if (x, y) in robots_step:
                    print('█', end="")
                else:
                    print(' ', end="")
            print()

    for step_num in range(10000):
        robots_step = simulate(step_num)
        meanx = sum(r[0] for r in robots_step) / len(robots_step)
        meany = sum(r[1] for r in robots_step) / len(robots_step)
