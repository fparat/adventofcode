#!/usr/bin/env python3

import sys

def is_big(cave):
    return cave.isupper()

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    graph = {}
    with open(filename) as f:
        for line in f:
            a, b = line.strip().split('-')
            graph.setdefault(a, []).append(b)
            graph.setdefault(b, []).append(a)

    paths = []

    def dfs(visited):
        for node in graph[visited[-1]]:
            visited2 = visited[:] + [node]
            if node == "end":
                paths.append(visited2)
            elif is_big(node) or node not in visited:
                dfs(visited2)

    dfs(["start"])

    print(f"Part 1: {len(paths)}")
