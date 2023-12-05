#!/usr/bin/env python3

import sys
import dataclasses
from typing import *

@dataclasses.dataclass
class Proj:
    src: int
    dst: int
    len: int

    def get(self, n: int) -> Optional[int]:
        if n in range(self.src, self.src + self.len):
            return self.dst + (n - self.src)


def parse(inp) -> Tuple[List[int], List[List[Proj]]]:
    lines = inp.splitlines()
    seeds = [int(n) for n in lines[0].split(':')[1].split()]
    
    maps = []
    current_map = []
    i = 2
    for line in lines[2:]:
        i += 1
        if ':' in line:
            assert not current_map, f"line {i}"
        elif not line.strip():
            assert current_map
            maps.append(current_map)
            current_map = []
        else:
            dst, src, length = [int(n) for n in line.split()]
            current_map.append(Proj(src, dst, length))
    
    if current_map:
        maps.append(current_map)

    return seeds, maps


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    seeds, maps = parse(inp)

    def location(seed):
        value = seed
        for map_ in maps:
            for proj in map_:
                new_value = proj.get(value)
                if new_value is not None:
                    value = new_value
                    break
        return value

    print(f"Part 1: {min(location(seed) for seed in seeds)}")
