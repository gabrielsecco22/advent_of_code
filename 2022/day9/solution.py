def read(filename):
    lines = open(filename).read().splitlines()
    return lines


def move(start_pos, direction, distance):
    # U D L R = up, down, left, right

    x, y = start_pos
    if direction == "U":
        y += distance
    elif direction == "D":
        y -= distance
    elif direction == "L":
        x -= distance
    elif direction == "R":
        x += distance

    return x, y


def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return max(abs(x1 - x2), abs(y1 - y2))

def get_move_vector(start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dx = x2 - x1
    dy = y2 - y1
    # limit size for both dx and dy to 1
    if dx != 0:
        dx = dx // abs(dx) #(dx = 5)
    if dy != 0:
        dy = dy // abs(dy)
    return dx, dy

def apply_vector(pos, vector):
    x, y = pos
    dx, dy = vector
    return x + dx, y + dy


class Rope:
    def __init__(self, start_pos, knots):
        self.knots = [start_pos] * knots
        self.visited = set()
        self.visited.add(start_pos)

    def move_one(self, direction):
        # U D L R = up, down, left, right
        """
        Move the rope 1 unit in the given direction
        If the knot(i) moves 2 positions afar from knot(i+1) then knot(i+1) moves to old knot(i) position
        Mark the last knot position as visited
        """
        self.knots[0] = move(self.knots[0], direction, 1)
        for i in range(len(self.knots) - 1):
            if get_distance(self.knots[i], self.knots[i+1]) > 1:
                vector = get_move_vector(self.knots[i+1], self.knots[i])
                self.knots[i+1] = apply_vector(self.knots[i+1], vector)

        self.visited.add(self.knots[-1])

    def move(self, direction, distance):
        for _ in range(distance):
            self.move_one(direction)


def sim_rope(filename, knots):
    lines = read(filename)
    start_pos = (0, 0)
    rope = Rope(start_pos, knots)
    for line in lines:
        direction, distance = line.split(" ")
        rope.move(direction, int(distance))
    return rope


if __name__ == "__main__":
    file = "input.txt"
    r1 = sim_rope(file, 2)
    r2 = sim_rope(file, 10)
    print(len(r1.visited))
    print(len(r2.visited))
