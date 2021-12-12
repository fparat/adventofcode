#!/usr/bin/env python3

import sys


def is_big(cave):
    return cave.isupper()


def is_small(cave):
    return cave not in ["start", "end"] and cave.islower()


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    # Parse graph

    graph = {}
    with open(filename) as f:
        for line in f:
            a, b = line.strip().split('-')
            graph.setdefault(a, []).append(b)
            graph.setdefault(b, []).append(a)


    # Part 1

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


    # Part 2

    paths = []

    def can_visit_small_twice(visited):
        smalls = [cave for cave in visited if is_small(cave)]
        return len(set(smalls)) == len(smalls)

    def dfs2(visited):
        for node in graph[visited[-1]]:
            visited2 = visited[:] + [node]
            if node == "end":
                paths.append(visited2)
            elif is_big(node) or node not in visited:
                dfs2(visited2)
            elif is_small(node) and can_visit_small_twice(visited):
                dfs2(visited2)

    dfs2(["start"])

    print(f"Part 2: {len(paths)}")
