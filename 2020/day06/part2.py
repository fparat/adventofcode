import string

if __name__ == "__main__":
    with open("input") as f:
        s = f.read()

    b = s.split("\n\n")
    a = [set(filter(str.isalpha, g)) for g in b]
    print(f"Part1: {sum(len(p) for p in a)}")

    n = []
    for r in b:
        m = []
        for g in r.splitlines():
            m.append(set(g))
        n.append(len(set.intersection(*m)))
    print(f"Part2: {sum(n)}")
