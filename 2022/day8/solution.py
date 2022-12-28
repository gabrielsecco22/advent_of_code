from random import randint
import matplotlib.pyplot as plt


def read(filename):
    lines = open(filename).read().splitlines()
    return lines


def gen_lines(h, w):
    lines = []
    for x in range(h):
        line = []
        for y in range(w):
            rand = randint(0, 9)
            line.append(rand)
        lines.append(line)
    return lines


class Map:
    def __init__(self, lines):
        self.lines = lines
        self.width = len(lines[0])
        self.height = len(lines)
        self.map = [[int(l[i]) for i in range(self.width)] for l in lines]
        self.max_in_lines = [[(x, i) for i, x in enumerate(self.map[y])] for y in range(self.height)]
        self.max_in_lines = [sorted(l, reverse=True) for l in self.max_in_lines]
        self.max_in_columns = [[(self.map[y][x], i) for i, y in enumerate(range(self.height))] for x in range(self.width)]
        self.max_in_columns = [sorted(c, reverse=True) for c in self.max_in_columns]

    def get(self, x, y):
        return self.map[x][y]

    def _is_border(self, x, y):
        if x == 0 or y == 0 or x == self.height - 1 or y == self.width - 1:
            return True
        return False

    def _is_h_h(self, x, y):
        # check if there greater or equal value is both left and right side
        m = self.map[x][y]
        found_left = False
        found_right = False
        for p in self.max_in_lines[x]:
            if p[0] >= m:
                if p[1] < y:
                    found_left = True
                elif p[1] > y:
                    found_right = True
            if found_left and found_right:
                return True
        return False

    def _is_v_h(self, x, y):
        # check if there greater or equal value is both top and bottom side
        m = self.map[x][y]
        found_top = False
        found_bottom = False
        for p in self.max_in_columns[y]:
            if p[0] >= m:
                if p[1] < x:
                    found_top = True
                elif p[1] > x:
                    found_bottom = True
            if found_top and found_bottom:
                return True
        return False

    def is_hidden(self, x, y):
        if self._is_border(x, y):
            return False
        else:
            h_h = self._is_h_h(x, y)
            v_h = self._is_v_h(x, y)
            return h_h and v_h

    def scenic_score(self, x, y):
        left, right, top, bottom = 0, self.width - 1, 0, self.height - 1
        if self._is_border(x, y):
            return 0, 0, 0, 0, 0
        else:
            for l in range(y - 1, -1, -1):
                if self.map[x][l] >= self.map[x][y]:
                    left = l
                    break
            for r in range(y + 1, self.height):
                if self.map[x][r] >= self.map[x][y]:
                    right = r
                    break
            for t in range(x - 1, -1, -1):
                if self.map[t][y] >= self.map[x][y]:
                    top = t
                    break
            for b in range(x + 1, self.width):
                if self.map[b][y] >= self.map[x][y]:
                    bottom = b
                    break
        l_s = y - left
        r_s = right - y
        t_s = x - top
        b_s = bottom - x
        s_s = l_s * r_s * t_s * b_s
        return s_s, l_s, r_s, t_s, b_s

    def is_visible(self, x, y):
        return not self.is_hidden(x, y)


def print_map(map: Map):
    format_space = 3
    # print top border
    print(" " * 3, end="")
    for i in range(map.width):
        print(f"{i:3d}", end="")
    print()
    for j, line in enumerate(map.map):
        print(f"{j:3d}", end="")
        print("".join([f"{x:3d}" for x in line]))


def fit_dist():
    values = []
    for i in range(3, 500):
        if i % 20 == 0:
            visible_total = 0
            N = 30
            for n in range(N):
                lines = gen_lines(i, i)
                m = Map(lines)
                # print_map(m)
                visible = 0
                for x in range(m.height):
                    for y in range(m.width):
                        visible += m.is_visible(x, y)
                visible_total += visible
            visible_avg = visible_total / N
            values.append((i, visible_avg, visible_avg / (i)))
            print(i, visible_avg, visible_avg / (i))

    # plot values
    # plt.plot([x[0] for x in values], [x[1] for x in values])
    plt.plot([x[0] for x in values], [x[2] for x in values])
    # plt.plot([x[0] for x in values], [x[3] for x in values])
    plt.show()


if __name__ == "__main__":
    # fit_dist()
    lines = read("input.txt")
    # lines = "30373,25512,65332,33549,35390"
    # lines = lines.split(",")
    # lines = gen_lines(10, 10)
    m = Map(lines)
    print_map(m)
    visible = 0
    max_score = 0
    max_score_pos = (0, 0)
    for x in range(m.height):
        for y in range(m.width):
            if m.is_visible(x, y):
                visible += 1
                # reason
                reason = ""
                if m._is_border(x, y):
                    reason += "border" if m._is_border(x, y) else ""
                else:
                    if not m._is_h_h(x, y) and not m._is_v_h(x, y):
                        reason += "both"
                    else:
                        reason += "horizontal" if not m._is_h_h(x, y) else ""
                        reason += "vertical" if not m._is_v_h(x, y) else ""
                # if reason != "border":
                # print(x, y, f"({m.get(x, y)})", reason)
            s_s, l, r, t, b = m.scenic_score(x, y)
            if s_s > max_score:
                max_score = s_s
                max_score_pos = (x, y)
                print(x, y, f"({m.get(x, y)})", s_s, l, r, t, b)

    # solution 1
    print(visible)

    # solution 2
    print(max_score_pos, max_score)
    # x, y = 86, 48
    # print(m.scenic_score(x, y))
    # print(m.is_visible(x, y), m._is_v_h(x, y), m._is_h_h(x, y))
