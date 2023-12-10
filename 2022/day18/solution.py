import queue


def read(filename):
    lines = open(filename).read().splitlines()
    return lines

def get_neighbors(pos, ds):
    x, y, z = pos
    for d in ds:
        x, y, z = d
        neighbors = [
            (x - 1, y, z),
            (x + 1, y, z),
            (x, y - 1, z),
            (x, y + 1, z),
            (x, y, z - 1),
            (x, y, z + 1)
        ]
        for n in neighbors:
            

class Node:
    def __init__(self, x, y, z, ds):
        self.name = str(f"{x}-{y}-{z}")
        self.visited = False
        self.nodes = []


def bfs(start):
    q = []
    q.append(start)
    start.visited = True
    while q:
        v = q.pop(0)
        for n in v.nodes:
            if not n.visited:
                q.append(n)
                n.visited = True




def solution1():
    ds = set()
    lines = read("input.txt")
    for line in lines:
        x, y, z = map(int, line.split(","))
        ds.add((x, y, z))

    r = 0

    for d in ds:
        n_count = 0
        x, y, z = d
        neighbors = [
            (x - 1, y, z),
            (x + 1, y, z),
            (x, y - 1, z),
            (x, y + 1, z),
            (x, y, z - 1),
            (x, y, z + 1)
        ]
        for n in neighbors:
            n_count += 1 if n in ds else 0

        r += 6 - n_count

    return r


def solution2():
    ds = set()
    lines = read("input.txt")
    for line in lines:
        x, y, z = map(int, line.split(","))



if __name__ == "__main__":
    print(solution2())
