#!/usr/bin/env python3

import sys
import string
from dataclasses import dataclass
from collections import namedtuple
from typing import *


Portal = namedtuple("Portal", ["name", "x", "y"])


@dataclass
class Map2D:
    cells: List[List[str]]

    @classmethod
    def from_str(cls, inp) -> "Map2D":
        return cls([list(line) for line in inp.splitlines()])

    def get(self, x, y):
        try:
            return self.cells[y][x]
        except IndexError:
            return " "

    def neighbours(self, x, y) -> Iterator[Tuple[int, int, str]]:
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx = x + dx
            ny = y + dy
            try:
                yield nx, ny, self.cells[ny][nx]
            except IndexError:
                pass


def parse_map(inp) -> Tuple[Dict[Portal, List[Tuple[Portal, int]]], Dict[Portal, Portal]]:
    map2d = Map2D.from_str(inp)

    portals = find_portals(map2d)

    connections = {}
    p2p = {}
    for (px, py), portal in portals.items():
        others = find_connected_portals(map2d, portals, px, py)

        for conn_name, (dist, cx, cy) in others.items():
            connections.setdefault(Portal(portal, px, py), []).append((Portal(conn_name, cx, cy), dist))

    for conn in connections:
        if conn in p2p:
            continue
        for conn2 in connections:
            if conn2 in p2p:
                continue
            if conn.name == conn2.name and conn != conn2:
                p2p[conn] = conn2
                p2p[conn2] = conn
                break

    return connections, p2p


def find_connected_portals(map2d: Map2D, portals, px, py):
    for x, y, p in map2d.neighbours(px, py):
        if p == ".":
            break

    other_portals = {}
    visited = set([(px, py)])

    def visit(x, y, dist=0):
        visited.add((x, y))
        for nx, ny, p in map2d.neighbours(x, y):
            if (nx, ny) in visited:
                continue
            if p == ".":
                visit(nx, ny, dist+1)
            elif p in string.ascii_uppercase:
                other_portals[portals[nx, ny]] = dist, nx, ny

    visit(x, y)

    return other_portals


def find_portals(map2d: Map2D):
    portals = {}

    for y, line in enumerate(inp.splitlines()):
        for x, c in enumerate(line):
            if c in string.ascii_uppercase:
                maze_path = None
                name = None
                for dx, dy in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
                    n = map2d.get(x + dx, y + dy)
                    if n == ".":
                        maze_path = (x, y)
                    if n in string.ascii_uppercase:
                        name = c + n if (dx + dy) > 0 else n + c
                if maze_path is not None:
                    portals[(x, y)] = name

    return portals


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    connections, p2p = parse_map(inp)

    for portal in connections:
        if portal.name == "AA":
            aa = portal
            break

    # Too lazy for Dijkstra, find all paths between AA and ZZ, then take the shortest
    dists = []
    visited = set()

    def explore(portal, dist=0):
        if portal in visited:
            return
        visited.add(portal)
        for conn, conn_dist in connections[portal]:
            if conn.name == "ZZ":
                dists.append(dist + conn_dist)
            elif conn.name != "AA":
                explore(p2p[conn], dist + conn_dist + 1)

    explore(aa)

    print(f"Part 1: {min(dists)}")
