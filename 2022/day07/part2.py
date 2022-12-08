from pathlib import PurePath
import sys
from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class File:
    name: str
    size: int


@dataclass
class Folder:
    name: str
    content: dict[str, Union["Folder", File]]

    def add_file(self, name, size):
        self.content[name] = File(name, size)

    def add_folder(self, name):
        self.content[name] = Folder(name, {})

    @property
    def size(self):
        return sum(item.size for item in self.content.values())


class Crawler:
    def __init__(self):
        self.root = Folder("/", {})
        self.cwd = PurePath("/")

    def get_folder(self, path) -> Folder:
        folder = self.root
        for part in path.parts[1:]:
            folder = folder.content[part]
            assert isinstance(folder, Folder)
        return folder

    def get_cwd(self) -> Folder:
        return self.get_folder(self.cwd)

    def update(self, command, output):
        toks = command.split()
        if toks[0] == "cd":
            if toks[1] == "/":
                self.cwd = PurePath("/")
            elif toks[1] == "..":
                self.cwd = self.cwd.parent
            else:
                self.cwd /= toks[1]
        elif toks[0] == "ls":
            for line in output:
                words = line.split()
                if words[0] == "dir":
                    self.get_cwd().add_folder(words[1])
                else:
                    self.get_cwd().add_file(words[1], int(words[0]))

    def print(self):
        print("/")
        def print_level(folder, path):
            for item in folder.content.values():
                if isinstance(item, File):
                    print(f"{item.size:<7} {path / item.name}")
                else:
                    print(f"dir     {path / item.name}/")
                    print_level(item, path / item.name)
        print_level(self.root, PurePath("/"))

    def walk(self, top=PurePath("/")):
        for item in self.get_folder(top).content.values():
            item_path = top / item.name
            yield item_path, item
            if isinstance(item, Folder):
                for subitem in self.walk(item_path):
                    yield subitem

    def get_dir_sizes(self):
        for path, item in self.walk():
            if isinstance(item, Folder):
                yield path, item.size


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1
    crawler = Crawler()
    history = [] # [(command, [output lines]), ...]
    command = None
    output = []
    for line in inp.splitlines():
        if line.startswith("$"):
            if command is not None:
                # # push current item and reset
                # history.append((command, output))
                crawler.update(command, output)
                output = []
            command = line[2:]
        else:
            output.append(line)

    crawler.print()

    thresh = 100000
    total = 0
    for path, size in crawler.get_dir_sizes():
        if size <= thresh:
            total += size
    print(f"Part 1: {total}")

    root_size = crawler.root.size
    total_size = 70000000
    free_size = total_size - root_size
    required_size = 30000000
    target = required_size - free_size
    to_delete = min(size for _, size in crawler.get_dir_sizes() if size >= target)
    print(f"Part 2: {to_delete}")
