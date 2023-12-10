from itertools import combinations

from fontTools.subset import intersect

VALVE_RELEASE_TIME = 1
TUNNEL_TRESPASS_TIME = 1


def read(filename):
    lines = open(filename).read().splitlines()
    return lines


class Valve:
    def __init__(self, name, release_value=None, adj_valves=None):
        self.name = name
        if adj_valves is not None:
            self.adj_valves = adj_valves
        if release_value is not None:
            self.release_value = release_value
        self.open = False
        self.visited = False
        self.dist = 99999999

    def release(self):
        self.open = True
        self.visited = True
        aux, self.release_value = self.release_value, 0
        return aux

    def visit(self, dist=None):
        self.visited = True
        if dist is not None:
            self.dist = min(self.dist, dist)

    def __repr__(self):
        return self.name


def build_graph(lines):
    valve_graph: dict[str, Valve] = {}
    start_valve = lines[0].split(" ")[1]

    for line in lines:
        # Parse line: Valve <name> has flow rate=<flow_rate>; tunnels lead to valves [<adj_valve1>, <adj_valve2>, ...]
        parts = line.split(" ")
        name = parts[1]
        flow_rate = int(parts[4].split("=")[-1].split(";")[0])
        sep = "valves " if "valves " in line else "valve "
        adj_valves = line.split(sep)[-1].split(", ")
        # create valve
        if name not in valve_graph:
            valve = Valve(name, flow_rate, [])
            valve_graph[name] = valve
        else:
            valve = valve_graph[name]
            valve.release_value = flow_rate
            valve.adj_valves = []

        for adj_valve in adj_valves:
            if adj_valve not in valve_graph:
                valve_graph[adj_valve] = Valve(adj_valve)
            valve_graph[name].adj_valves.append(valve_graph[adj_valve])

    # valve_graph["start"] = valve_graph[start_valve]
    return valve_graph


def vg_distance(vg, s):
    vg_reset(vg)
    start = vg[s]
    queue = [start]
    start.visit(0)
    while queue:
        current = queue.pop(0)
        d = current.dist + 1
        for adj in current.adj_valves:
            if not adj.visited:
                queue.append(adj)
                adj.visit(d)
    return vg


def vg_get_max(vg, s, t):
    vg_distance(vg, s)
    # maximize the pressure released by consumed time
    # Pressure Released: (t - v.dist - 1) * v.release_value
    # Time Consumed: v.dist + 1
    m = max([(v, (t - v.dist - 1) * v.release_value, v.dist + 1) for v in vg.values() if not v.open], key=lambda x: x[1] / x[2])
    if m[1] > 0:
        m[0].open = True
        return m, t - m[0].dist - 1, m[0].name
    else:
        return -1, -1, s


def vg_get_sorted(vg, s, t, path=[]):
    vg_distance(vg, s)
    # maximize the pressure released by consumed time
    # Pressure Released: (t - v.dist - 1) * v.release_value
    # Time Consumed: v.dist + 1
    m = sorted([(v, (t - v.dist - 1) * v.release_value, v.dist + 1) for v in vg.values() if v.name not in path and v.release_value > 0], key=lambda x: x[1] / x[2], reverse=True)
    if len(m) > 0:
        max = m[0][1] / m[0][2]
        m = [x for x in m if x[1] / x[2] > max * 0.5]
        return m
    return -1


def vg_reset(vg):
    for v in vg.values():
        v.visited = False
        v.dist = 99999999


def vg_reset_all(vg):
    for v in vg.values():
        v.visited = False
        v.dist = 99999999
        v.open = False


def p1_old(lines):
    v_g = build_graph(lines)
    st = "AA"
    t = 30
    s = 0
    rate = 0
    vg_get_sorted(v_g, st, t)
    while t > 0:
        m1, t, x = vg_get_max(v_g, st, t)
        if m1 == -1:
            break
        s += m1[1]
        rate += m1[0].release_value
        print(st, f"{t + m1[0].dist + 1:2d}", m1, m1[0].dist, f"{m1[0].release_value:2d}", t, f"{s:4d}", f"{rate:4d}", sep="-\t--")
        st = m1[0].name
    print(s)


def p1(lines, t=30):
    v_g = build_graph(lines)
    st = "AA"

    def r(vert=st, cost=0, path=[], r_p=0):
        m = vg_get_sorted(v_g, vert, t - cost, path)
        if cost > t:
            return
        if m == -1 or len(m) == 0:
            # print(r_p, path, cost)
            yield cost, path, r_p
        else:
            for v, rp, d in m:
                if v.name in path:
                    continue
                # print(f"Walk from {vert} - Release {v.name} at a cost of {d} with {v.release_value}*{t - cost - d}={rp} pressure, Remaining time {t - cost - d}")
                yield from r(v.name, cost + d, path + [v.name], r_p + rp)

    return [(x[0], x[1], x[2]) for x in sorted(r(), key=lambda x: x[2], reverse=True)]


def p2(lines, t=26):
    v_g = build_graph(lines)
    st = ["AA", "AA"]
    ms = [0, 0]

    def r(vert, cost=[0, 0], path=[], r_p=0):
        # print(vert, cost, path, r_p)
        for i in range(len(vert)):
            m = vg_get_sorted(v_g, vert[i], t - cost[i], path)
            if cost[i] > t:
                continue
            if m == -1 or len(m) == 0:
                ms[i] = -1
                if ms == [-1, -1]:
                    print(r_p, path, cost)
                    yield cost, path, r_p
            else:
                for v, rp, d in m:
                    if v.name in path:
                        continue
                    # print(f"Walk from {vert} - Release {v.name} at a cost of {d} with {v.release_value}*{t - cost - d}={rp} pressure, Remaining time {t - cost - d}")
                    vert[i] = v.name
                    cost[i] += d
                    yield from r(vert, cost, path + [v.name], r_p + rp)

    return [(x[0], x[1], x[2]) for x in sorted(r(st), key=lambda x: x[2], reverse=True)]


if __name__ == "__main__":
    filename = "input.txt"
    lines = read(filename)
    pts = p1(lines, 30)
    print(pts[0])
    pts2 = p1(lines, 26)
    max_sum = 0
    for (c1, p1, v1), (c2, p2, v2) in combinations(pts2, 2):
        if not(set(p1).intersection(set(p2))) and v1 + v2 > max_sum:
            print(c1,p1,v1, c2,p2,v2)
            max_sum = v1 + v2
        if max_sum > 2*v1 and max_sum > 2*v2:
            break
    print(max_sum)


