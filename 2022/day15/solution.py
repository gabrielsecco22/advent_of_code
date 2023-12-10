import re


def m_d(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def read(filename):
    lines = open(filename).read().splitlines()
    return lines


def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = []
    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], interval[1]))
    return merged


def in_intervals(intervals, y):
    for interval in intervals:
        if interval[0] <= y <= interval[1]:
            return True
    return False


class Sensor:
    def __init__(self, pos, nearest_beacon):
        self.pos = pos
        self.nearest_beacon = nearest_beacon
        self.range = m_d(pos, nearest_beacon)

    def update_range(self, pos):
        self.range = max(self.range, m_d(self.pos[0], self.pos[1], pos[0], pos[1]))

    def in_range(self, pos1):
        return m_d(self.pos, pos1) <= self.range

    def get_interval_at(self, y):
        dist = m_d(self.pos, (self.pos[0], y))
        if dist <= self.range:
            left = self.pos[0] - self.range + dist
            right = self.pos[0] + self.range - dist
            return left, right
        else:
            return None

    def get_tunning_vector(self, pos1):
        return self.pos[0] - pos1[0], self.pos[1] - pos1[1]


class Map:
    def __init__(self, s, b):
        self.sensors = s
        self.beacons = b

    def get_no_beacon_intervals(self, y):
        intervals = []
        for sensor in self.sensors:
            intervals.append(sensor.get_interval_at(y))
        return [x for x in intervals if x is not None]

    def get_sensor_by_pos(self, pos):
        for sensor in self.sensors:
            if sensor.pos == pos:
                return sensor
        return None

    def get_beacons_in_ranges(self, y):
        ranges = merge_intervals(self.get_no_beacon_intervals(y))
        beacons = []
        for r in ranges:
            for b in self.beacons:
                if r[0] <= b[0] <= r[1] and b[1] == y:
                    beacons.append(b)
        return beacons

    def get_not_beacon_positions(self, y):
        merged = merge_intervals(self.get_no_beacon_intervals(y))
        a = sum([x[1] - x[0] + 1 for x in merged])
        b = self.get_beacons_in_ranges(y)
        return a - len(b)

    def can_be_beacon(self, pos):
        x, y = pos
        if not 0 <= x <= 4000000 or not 0 <= y <= 4000000:
            return False
        if pos in self.beacons:
            return False
        for sensor in self.sensors:
            if sensor.in_range(pos):
                return False
        return True

    def find_blind_spot(self):
        """
        Find the spot with no sensor in range
        1 - generate 4 lines for each sensor from manhattan distance to the sensor to the max range + 1
        2 - aggregate the lines using angular coefficient and intercept as keys
        3 - find intersections between rising lines and falling lines
        4 - test intersections as candidates
        """
        lines: dict[tuple[int, int], int] = {} # line: y = a * x + b -> dict key: (a, b) -> dict value: count

        for sensor in self.sensors:
            """
            Sensor boundary lines (range + 1)
            Follow circle quadrants
            line 1 : upper right a = -1, b = y - r + x
            line 2 : upper left a = 1, b = y - r - x
            line 3 : lower left a = -1, b = y + r + x
            line 4 : lower right a = 1, b = y + r - x
            """
            r = sensor.range + 1
            x, y = sensor.pos

            a_s = [-1, 1, -1, 1]
            b_s = [y - r + x, y - r - x, y + r + x, y + r - x]
            for i in range(4):
                a = a_s[i]
                b = b_s[i]
                line = (a, b)
                if line in lines:
                    lines[line] += 1
                else:
                    lines[line] = 1

        a_positive_lines: list[int] = []
        a_negative_lines: list[int] = []
        for line, count in lines.items():
            if count > 1:
                if line[0] > 0:
                    a_positive_lines.append(line[1])
                else:
                    a_negative_lines.append(line[1])

        candidates: list[tuple[int, int]] = []
        for rising in a_positive_lines:
            for falling in a_negative_lines:
                # line intersection: y_r = x + b_r, y_f = -x + b_f
                # x = (b_f - b_r) / 2
                x = (falling - rising) // 2
                y = x + rising
                candidates.append((x, y))

        for candidate in candidates:
            if self.can_be_beacon(candidate):
                return candidate

    def print(self):
        spot = None
        for y in range(-2, 23):
            merged = merge_intervals(self.get_no_beacon_intervals(y))
            for x in range(-2, 26):
                if (x, y) in self.beacons:
                    print("B", end="")
                elif self.get_sensor_by_pos((x, y)) is not None:
                    print("S", end="")
                else:
                    if in_intervals(merged, x):
                        print("#", end="")
                    else:
                        if 0 <= x <= 20 and 0 <= y <= 20:
                            spot = (x, y)
                        print(".", end="")
            print()
        print(spot)


def build_map(lines):
    sensors = set()
    beacons = set()
    for line in lines:
        # line = Sensor at x=<xs>, y=<ys>: closest beacon is at x=<xb>, y=<yb>
        xs, ys, xb, yb = map(int, re.findall(r"-?\d+", line))
        sensors.add(Sensor((xs, ys), (xb, yb)))
        beacons.add((xb, yb))
    return Map(sensors, beacons)


def solve1(lines, y):
    mp = build_map(lines)
    return mp.get_not_beacon_positions(y)


def solve2(lines):
    mp = build_map(lines)
    a = mp.find_blind_spot()
    print(a[0] * 4000000 + a[1])


if __name__ == "__main__":
    lines = read("input.txt")
    print(solve1(lines, 2000000))
    solve2(lines)
