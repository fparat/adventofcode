import string

if __name__ == "__main__":
    with open("input") as f:
        s = f.read()

    b = s.split("\n\n")
    a = [set(filter(str.isalpha, g)) for g in b]
    print(f"Part1: {sum(len(p) for p in a)}")
