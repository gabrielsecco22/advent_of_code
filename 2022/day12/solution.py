def read(filename):
    lines = open(filename).read().splitlines()
    return lines


def height_value(pos, map):
    y, x = pos
    v = map[y][x]
    if v == "E":
        return ord("z")
    if v == "S":
        return ord("a")
    return ord(v)


def height_diff(pos1, pos2, map):
    return height_value(pos2, map) - height_value(pos1, map)


def get_start_pos(map):
    return [(y, x) for x in range(len(map[0])) for y in range(len(map)) if map[y][x] == "S"][0]


def min_path(steps, curr_pos, map, visited, memo):

    visited.add(curr_pos)
    y, x = curr_pos
    v = map[y][x]
    if memo[y][x] != 0:
        if memo[y][x] > steps:
            memo[y][x] = steps
    else:
        memo[y][x] = steps
    if v == "E":
        return steps

    new_pos = [(y, x + 1), (y + 1, x), (y - 1, x), (y, x - 1)]
    new_pos = [pos for pos in new_pos if 0 <= pos[0] < len(map) and 0 <= pos[1] < len(map[0])]
    new_pos = [pos for pos in new_pos if pos not in visited]
    new_pos = [pos for pos in new_pos if height_diff(curr_pos, pos, map) <= 1]
    if not new_pos:
        # return a large number
        return 1_000_000

    return min([min_path(steps + 1, pos, map, visited, memo) for pos in new_pos])


def main():
    lines = read("input.txt")
    map = [list(line) for line in lines]
    start_pos = get_start_pos(map)
    visited = set()
    visited.add(start_pos)
    memo = [[0 for _ in range(len(map[0]))] for _ in range(len(map))]
    print(min_path(0, start_pos, map, visited, memo))


if __name__ == "__main__":
    main()
