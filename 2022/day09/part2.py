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

    def update_head(self, direction):
        match direction:
            case "U":
                self.head = (self.head[0], self.head[1] - 1)
            case "D":
                self.head = (self.head[0], self.head[1] + 1)
            case "L":
                self.head = (self.head[0] - 1, self.head[1])
            case "R":
                self.head = (self.head[0] + 1, self.head[1])

    def update_tail(self):
        dx = self.head[0] - self.tail[0] # head relative to tail
        dy = self.head[1] - self.tail[1]

        if dx == 0: # is up or down
            dtail = (0, ((dy//abs(dy)) if abs(dy) > 1 else 0))
        elif dy == 0: # is left or right
            dtail = (((dx//abs(dx)) if abs(dx) > 1 else 0), 0)
        elif abs(dx) > 1 or abs(dy) > 1: # diagonal
            dtail = (dx//abs(dx), dy//(abs(dy)))
        else:
            dtail = (0, 0)

        self.tail = (self.tail[0] + dtail[0], self.tail[1] + dtail[1])

        self.visited.add(self.tail)

        # self.draw()
        assert abs(dtail[0]) <= 1
        assert abs(dtail[1]) <= 1

    def motion(self, direction):
        self.update_head(direction)
        self.update_tail()


class MultiState:
    def __init__(self, rope_size=10):
        # [0] is head
        self.states = [State() for _ in range(rope_size)]

    def motion(self, direction):
        # update the first state, then copy its tail to head of second state, and repeat
        self.states[0].motion(direction)
        for n in range(1, len(self.states)):
            self.states[n].head = self.states[n-1].tail
            self.states[n].update_tail()

        # self.draw()

    @property
    def visited(self):
        return self.states[-2].visited

    def draw(self):
        min_x = min(min(s.head[0] for s in self.states), min(s.tail[0] for s in self.states), min(v[0] for v in self.visited))
        max_x = max(max(s.head[0] for s in self.states), max(s.tail[0] for s in self.states), max(v[0] for v in self.visited))
        min_y = min(min(s.head[1] for s in self.states), min(s.tail[1] for s in self.states), min(v[1] for v in self.visited))
        max_y = max(max(s.head[1] for s in self.states), max(s.tail[1] for s in self.states), max(v[1] for v in self.visited))

        for y in range(min_y, max_y+1):
            for x in range(min_x, max_x+1):
                for n, state in enumerate(self.states):
                    if (x, y) == state.head:
                        print("H" if n == 0 else str(n), end="")
                        break
                    elif (x, y) == state.tail and n == len(self.states) - 1:
                        print("T", end="")
                        break
                    elif (x, y) == (0, 0):
                        print("s", end="")
                        break
                    elif (x, y) in self.visited:
                        print("#", end="")
                        break
                else:
                    print(".", end="")
            print()
        print()



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

    # Part 2

    multistate = MultiState(10)
    for direction, num in motions:
        for n in range(num):
            multistate.motion(direction)
    print(f"Part 2: {len(multistate.visited)}")
