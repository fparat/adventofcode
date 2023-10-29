#!/usr/bin/env python3

import heapq
from queue import PriorityQueue
import sys
import string
from dataclasses import dataclass, field
from collections import deque, namedtuple
from typing import *


OUTER = -1
INNER = 1


width = None # lazy init
heigth = None # lazy init

Portal = namedtuple("Portal", ["name", "x", "y"])
def get_io(p: Portal):
    return OUTER if p.x < 4 or p.x > width-4 or p.y < 4 or p.y > heigth-4 else INNER
Portal.io = get_io


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

    global width, heigth
    heigth = len(map2d.cells)
    width = len(map2d.cells[0])

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


@dataclass(order=True)
class PriorityItem:
    dist: int
    level: int = field(compare=False)
    portal: Portal = field(compare=False)

class PriorityQueue:
    def __init__(self):
        self.dists = {}
        self.queue = []

    def put(self, dist, level, portal):
        self.dists[(level, portal)] = dist
        heapq.heappush(self.queue, PriorityItem(dist, level, portal))

    def pop(self) -> Tuple[int, int, Portal]:
        item = heapq.heappop(self.queue)
        del self.dists[(item.level, item.portal)]
        return item.dist, item.level, item.portal

    def get(self, level, portal):
        try:
            return self.dists[(level, portal)], level, portal
        except KeyError:
            return None, None, None

    def replace(self, dist, level, portal):
        print("replace")
        for idx, item in enumerate(self.queue):
            if (level, portal) == (item.level, item.portal):
                self.dists[(level, portal)] = dist
                self.queue[idx] = PriorityItem(dist, level, portal)
                break
        heapq.heapify(self.queue)

    def __repr__(self):
        return f"{self.queue!r}"


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

    # Part 2

    def explore2(portal):
        level = 0
        dist = 0
        frontier = PriorityQueue()
        frontier.put(dist, level, portal)
        visited = set()

        while True:
            dist, level, portal = frontier.pop()

            # print(f"{str(portal):<32} {level=:<4} {dist=} {[(p[0].name, p[1]) for p in connections[portal]]}")
            visited.add((level, portal))

            for conn, conn_dist in connections[portal]:
                new_dist = dist + conn_dist + 1
                if conn.name == "ZZ":
                    if level == 0:
                        dists.append(new_dist - 1)
                        return new_dist - 1
                    continue
                elif conn.name == "AA" or (level == 0 and conn.io() == OUTER):
                    continue
                new_level = level + conn.io()

                previous_dist, previous_level, previous_portal = frontier.get(new_level, p2p[conn])
                if (new_level, p2p[conn]) not in visited and previous_portal is None:
                    frontier.put(new_dist, new_level, p2p[conn])
                elif previous_dist is not None and previous_dist > new_dist:
                    frontier.replace(new_dist, new_level, conn)

    print(f"Part 2: {explore2(aa)}")
