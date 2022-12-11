import sys


class State:
    def __init__(self):
        # (x, y)
        # .-> x
        # |
        # v  y
        self.head = (0, 0)
        self.tail = (0, 0)
        self.visited = set([self.tail])

    def draw(self):
        min_x = min(self.head[0], self.tail[0], min(v[0] for v in self.visited))
        max_x = max(self.head[0], self.tail[0], max(v[0] for v in self.visited))
        min_y = min(self.head[1], self.tail[1], min(v[1] for v in self.visited))
        max_y = max(self.head[1], self.tail[1], max(v[1] for v in self.visited))

        for y in range(min_y, max_y+1):
            for x in range(min_x, max_x+1):
                if (x, y) == self.head:
                    print("H", end="")
                elif (x, y) == self.tail:
                    print("T", end="")
                elif (x, y) == (0, 0):
                    print("s", end="")
                elif (x, y) in self.visited:
                    print("#", end="")
                else:
                    print(".", end="")
            print()
        print()

    def motion(self, direction):
        # update head
        match direction:
            case "U":
                self.head = (self.head[0], self.head[1] - 1)
            case "D":
                self.head = (self.head[0], self.head[1] + 1)
            case "L":
                self.head = (self.head[0] - 1, self.head[1])
            case "R":
                self.head = (self.head[0] + 1, self.head[1])

        # update tail
        dx = self.head[0] - self.tail[0] # head relative to tail
        dy = self.head[1] - self.tail[1]

        if dx == 0: # is up or down
            self.tail = (self.tail[0], self.tail[1] + ((dy//abs(dy)) if abs(dy) > 1 else 0))
        elif dy == 0: # is left or right
            self.tail = (self.tail[0] + ((dx//abs(dx)) if abs(dx) > 1 else 0), self.tail[1])
        elif abs(dx) > 1 or abs(dy) > 1: # diagonal
            self.tail = (self.tail[0] + dx//abs(dx), self.tail[1] + dy//(abs(dy)))

        self.visited.add(self.tail)

        # self.draw()


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "input"

    with open(filename) as f:
        inp = f.read()

    # Part 1

    motions = []
    for line in inp.splitlines():
        m = line.split()
        motions.append((m[0], int(m[1])))

    state = State()
    for direction, num in motions:
        for n in range(num):
            state.motion(direction)

    print(f"Part 1: {len(state.visited)}")
