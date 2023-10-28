#!/usr/bin/env python3

import sys
import string
import functools
import heapq
from dataclasses import dataclass, field
from collections import deque
from typing import Dict, Iterable, List, Iterator, Tuple

if not hasattr(functools, "cache"):
    # monkey patch for pypy3
    def cache(user_function, /):
        return functools.lru_cache(maxsize=None)(user_function)
    functools.cache = cache


ENTRANCE = '@'
WALL = '#'
OPEN = '.'
KEYS = string.ascii_lowercase
DOORS = string.ascii_uppercase

PARSE_TREE_VALID = OPEN + KEYS + DOORS


import sys
sys.setrecursionlimit(2000)


@dataclass
class Node:
    c: str
    x: int
    y: int
    nb: Dict[Tuple[int, int], "Node"] = field(default_factory=dict) # neighbours

    def __repr__(self):
        return f"({self.x} {self.y} {self.c} [{len(self.nb)}])"

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def link(self, other: "Node"):
        self.nb[other.x, other.y] = other
        other.nb[self.x, self.y] = self

    @functools.cache
    def items(self, opened_doors=()) -> List[List["Node"]]:
        return list(self.iter_items(opened_doors))

    def iter_items(self, opened_doors=()) -> Iterator[List["Node"]]:
        for path in self.bfs():
            c = path[-1].c
            if c.isalpha() and all(not node.c.isupper() or node.c in opened_doors for node in path[:-1]):
                yield path

    def keys(self, opened_doors=()) -> Iterator[List["Node"]]:
        return (path for path in self.items(opened_doors) if path[-1].c in KEYS)

    def doors(self, opened_doors=()) -> Iterator[List["Node"]]:
        return (path for path in self.items(opened_doors) if path[-1].c in DOORS)

    @functools.cache
    def bfs(self) -> List[List["Node"]]:
        return list(self.iter_bfs())

    def iter_bfs(self) -> Iterator[List["Node"]]:
        parents = {self: None}

        def path(self) -> List["Node"]:
            path = [self]
            current = self
            while parents[current] is not None:
                current = parents[current]
                path.append(current)
            return list(reversed(path))

        q = deque()
        found = set([self])
        q.append(self)
        while q:
            node = q.popleft()
            yield path(node)
            for nb in node.nb.values():
                if nb not in found:
                    found.add(nb)
                    parents[nb] = node
                    q.append(nb)


@dataclass
class Map2D:
    cells: List[List[str]]

    def neighbours(self, node: Node) -> Iterator[Tuple[int, int, str]]:
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            try:
                x = node.x + dx
                y = node.y + dy
                yield x, y, self.cells[y][x]
            except IndexError:
                pass

    def find_entrance(self) -> Node:
        for x, row in enumerate(self.cells):
            for y, c in enumerate(row):
                if c == ENTRANCE:
                    return Node(c, x, y)
        raise ValueError("Entrance not found")

    def patch_part2(self) -> List[Node]:
        root = self.find_entrance()
        map2d.cells[root.y-1][root.x-1] = ENTRANCE
        map2d.cells[root.y-1][root.x+0] = WALL
        map2d.cells[root.y-1][root.x+1] = ENTRANCE
        map2d.cells[root.y+0][root.x-1] = WALL
        map2d.cells[root.y+0][root.x+0] = WALL
        map2d.cells[root.y+0][root.x+1] = WALL
        map2d.cells[root.y+1][root.x-1] = ENTRANCE
        map2d.cells[root.y+1][root.x+0] = WALL
        map2d.cells[root.y+1][root.x+1] = ENTRANCE

        return [
            Node(ENTRANCE, root.x-1, root.y-1),
            Node(ENTRANCE, root.x+1, root.y-1),
            Node(ENTRANCE, root.x-1, root.y+1),
            Node(ENTRANCE, root.x+1, root.y+1),
        ]


def clean_keys(*keys_list: Iterable[str]):
    all_keys = set()
    for keys in keys_list:
        for key in keys:
            all_keys.add(key)
    return ''.join(sorted(all_keys))


next_state_cache = {}

@dataclass
class State:
    x: Tuple[int]
    y: Tuple[int]
    keys: str = ""

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.keys))

    def new_state(self, i, x, y, keys) -> "State":
        newx = list(self.x)
        newy = list(self.y)
        newx[i] = x
        newy[i] = y
        return State(x=tuple(newx), y=tuple(newy), keys=keys)

    def opened(self):
        return self.keys.upper()

    def next_states(self, nodes: Dict[Tuple[int, int], Node]) -> List[Tuple["State", int]]:
        nstates = next_state_cache.get(self)
        if nstates is None:
            nstates = list(self.iter_next_states(nodes))
            next_state_cache[self] = nstates
        return nstates

    def iter_next_states(self, nodes: Dict[Tuple[int, int], Node]) -> Iterator[Tuple["State", int]]:
        for i in range(len(self.x)):
            for path in nodes[self.x[i], self.y[i]].keys(self.opened()):
                new_keys = [node.c for node in path if node.c in KEYS and node.c not in self.keys]
                if not new_keys:
                    continue # already have all keys
                new_state = self.new_state(i, path[-1].x, path[-1].y, clean_keys(self.keys, new_keys))
                cost = len(path) - 1
                yield new_state, cost


@dataclass(order=True)
class PriorityItem:
    cost: int
    state: State = field(compare=False)

class PriorityQueue:
    def __init__(self):
        self.costs = {}
        self.queue = []

    def _sort(self):
        self.queue.sort(key=lambda x: x[0], reverse=True)

    def put(self, cost, state):
        self.costs[state] = cost
        heapq.heappush(self.queue, PriorityItem(cost, state))

    def pop(self) -> Tuple[int, State]:
        item = heapq.heappop(self.queue)
        del self.costs[item.state]
        return item.cost, item.state

    def get(self, state):
        try:
            return self.costs[state], state
        except KeyError:
            return None, None

    def replace(self, cost, state):
        for idx, item in enumerate(self.queue):
            if state == item.state:
                self.costs[state] = cost
                self.queue[idx] = PriorityItem(cost, state)
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

    map2d = Map2D(list(list(line) for line in inp.splitlines()))

    root = map2d.find_entrance()
    nodes = {(root.x, root.y): root}

    def parse_neighbours(node: Node, map2d: Map2D):
        for x, y, c in map2d.neighbours(node):
            if c in PARSE_TREE_VALID and (x, y) not in node.nb:
                prev = nodes.get((x, y))
                if prev is not None:
                    node.link(prev)
                    continue
                new_node = Node(c, x, y)
                nodes[x, y] = new_node
                node.link(new_node)
                parse_neighbours(new_node, map2d)

    parse_neighbours(root, map2d)

    all_keys = ''.join(sorted(c for c in inp if c in KEYS))
    root_state = State((root.x,), (root.y,))

    def find_cheapest(self: State) -> int:
        # Dijkstra - Uniform-cost search
        found = set()
        frontier = PriorityQueue()
        frontier.put(0, self)

        while True:
            state_cost, state = frontier.pop()
            # print(f"{state_cost:<5} {state.keys}")

            if state.keys == all_keys:
                return state_cost

            found.add(state)

            for nstate, cost in state.next_states(nodes):
                previous_cost, previous_state = frontier.get(nstate)
                if nstate not in found and previous_state is None:
                    frontier.put(cost + state_cost, nstate)
                elif previous_cost is not None and previous_cost > (cost + state_cost):
                    frontier.replace(cost + state_cost, nstate)

    print(f"Part 1: {find_cheapest(root_state)}")

    # Part 2

    next_state_cache.clear()
    roots = map2d.patch_part2()
    nodes = {
        (root.x, root.y): root
        for root in roots
    }

    for root in roots:
        parse_neighbours(root, map2d)


    root_state = State(
        x=(roots[0].x, roots[1].x, roots[2].x, roots[3].x,),
        y=(roots[0].y, roots[1].y, roots[2].y, roots[3].y,),
    )

    print(f"Part 2: {find_cheapest(root_state)}")
