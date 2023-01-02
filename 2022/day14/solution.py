import re
import time


def read(filename):
    lines = open(filename).read().splitlines()
    return lines


def my_range(start, end, step):
    if abs(end - (start + step)) > abs(end - start):
        return reversed(range(end, start + step, step))
    else:
        return range(start, end + step, step)


class Cavern:
    def __init__(self, rock_tiles, sand_pour_points):
        self.sand_pour_points = sand_pour_points
        self.rock_tiles = rock_tiles
        self.sand_tiles = set()
        self.settled_sand_tiles = set()
        self.steps = 0

    def add_floor(self):
        floor_level = max([p[1] for p in self.rock_tiles]) + 2
        h = floor_level - min(p[1] for p in self.sand_pour_points)
        x1 = min(p[0] for p in self.sand_pour_points) - h - 10
        x2 = max(p[0] for p in self.sand_pour_points) + h + 10
        self.insert_line((x1, floor_level), (x2, floor_level), "rock")

    def depth(self, point):
        d = 0
        while True:
            d += 1
            below = (point[0], point[1] + d)
            if below in self.rock_tiles or below in self.settled_sand_tiles:
                return d - 1
            if below[1] > max([p[1] for p in self.rock_tiles]):
                return -1
            if d > 200:
                print("Too deep")

    def insert(self, point, type):
        if type == "settled_sand":
            self.settled_sand_tiles.add(point)
        elif type == "sand":
            self.sand_tiles.add(point)
        elif type == "rock":
            self.rock_tiles.add(point)
        else:
            raise Exception("Invalid type")

    def insert_line(self, p1, p2, type):
        x1, y1 = p1
        x2, y2 = p2
        if x1 == x2:
            step = 1 if y1 < y2 else -1
            for y in my_range(y1, y2, step):
                self.insert((x1, y), type)
        elif y1 == y2:
            step = 1 if x1 < x2 else -1
            for x in my_range(x1, x2, step):
                self.insert((x, y1), type)
        else:
            raise Exception("Invalid line")

    def settle_sand(self, point):
        stack = [point]
        while len(stack) > 0:
            p = stack.pop()
            if self.depth(p) == -1:
                return -1
            x, y = p
            left_below = (x - 1, y + 1)
            right_below = (x + 1, y + 1)
            below = (x, y + 1)
            stack.append(right_below)
            stack.append(left_below)
            stack.append(below)
            invalids = [pt for pt in [below, left_below, right_below] if pt in self.rock_tiles or pt in self.settled_sand_tiles]
            for invalid in invalids:
                stack.remove(invalid)
            if len(invalids) == 3:
                self.insert(p, "settled_sand")
                return p
        return None

    def step(self):
        has_next = True
        for sp in self.sand_pour_points:
            self.insert(sp, "sand")
        for s in self.sand_tiles:
            depth = self.depth(s)
            if depth == -1:
                has_next = False
                break
            settle_point = (s[0], s[1] + depth)
            r = self.settle_sand(settle_point)
            if r == -1 or r in self.sand_pour_points:
                has_next = False
                break
        self.sand_tiles = set()
        return has_next

    def simulate(self):
        start_time = time.time()
        while self.step():
            self.steps += 1
            if self.steps % 100 == 0:
                end_time = time.time()
                print("Step: {}, Time: {}".format(self.steps, end_time - start_time))
                start_time = time.time()
                print(f"Step {self.steps}")

    def print(self, left_top=None, right_bottom=None):
        if left_top is None:
            left_top = (min([p[0] for p in self.rock_tiles]), min([p[1] for p in self.rock_tiles] + [p[1] for p in self.sand_pour_points]))
        if right_bottom is None:
            right_bottom = (max([p[0] for p in self.rock_tiles]), max([p[1] for p in self.rock_tiles] + [p[1] for p in self.sand_pour_points]))

        for y in range(left_top[1], right_bottom[1] + 1):
            for x in range(left_top[0], right_bottom[0] + 1):
                if (x, y) in self.rock_tiles:
                    print("#", end="")
                elif (x, y) in self.settled_sand_tiles:
                    print("o", end="")
                elif (x, y) in self.sand_tiles:
                    print("+", end="")
                else:
                    print(".", end="")
            print()
        print()
        print()


if __name__ == "__main__":
    lines = read("input.txt")
    sand_pour_points = [(500, 0)]
    cavern = Cavern(set(), sand_pour_points)
    for line in lines:
        rock_lines = line.split(" -> ")
        rock_vertices = []
        for rl in rock_lines:
            px, py = map(int, re.findall(r"\d+", rl))
            rock_vertices.append((px, py))
        for i in range(len(rock_vertices) - 1):
            cavern.insert_line(rock_vertices[i], rock_vertices[i + 1], "rock")
    # cavern.insert((500, 8), "settled_sand")
    cavern.simulate()
    print(len(cavern.settled_sand_tiles))
    cavern.add_floor()
    cavern.print()
    cavern.simulate()
    cavern.print()
    print(len(cavern.settled_sand_tiles))
