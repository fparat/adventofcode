#!/usr/bin/env python3
# coding: utf-8


if __name__ == "__main__":
    with open("input") as f:
        s = f.read()

    # Parse
    rules = {}
    for line in s.splitlines():
        container, contained_desc = line.strip(".").split(" bags contain ")
        contained = {}
        if contained_desc != "no other bags":
            contained_objs = contained_desc.split(", ")
            for obj in contained_objs:
                num, name = obj.split(maxsplit=1)
                contained[name.rsplit(maxsplit=1)[0]] = int(num)
        rules[container] = contained

    # Part 1
    found = set()

    def collect(name):
        bags = rules[name]
        if "shiny gold" in bags:
            found.add(name)
        for bag in bags.keys():
            if collect(bag):
                found.add(name)
        return name in found

    for name in rules:
        collect(name)

    print(f"Part 1: {len(found)}")


    # Part 2

    def count(name):
        localcount = 0
        for bag, num in rules[name].items():
            localcount += num * (count(bag) + 1)
        return localcount

    print(f"Part 2: {count('shiny gold')}")
