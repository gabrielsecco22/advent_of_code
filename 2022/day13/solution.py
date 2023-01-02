import functools


def read(filename):
    lines = open(filename).read().splitlines()
    return lines


def compare_elem(a, b):
    if a == b:
        return 0
    if a is None and b is not None:
        return 1
    if a is not None and b is None:
        return -1
    if isinstance(a, list) and isinstance(b, list):
        return compare(a, b)
    elif isinstance(a, int) and isinstance(b, list):
        new_list = [a]
        return compare(new_list, b)
    elif isinstance(a, list) and isinstance(b, int):
        new_list = [b]
        return compare(a, new_list)
    else:
        return (a <= b) - (a >= b)


def compare(list1, list2):
    if list1 == list2:
        return 0
    size = max(len(list1), len(list2))
    for i in range(size):
        a = list1[i] if i < len(list1) else None
        b = list2[i] if i < len(list2) else None
        c = compare_elem(a, b)
        if c != 0:
            return c
    return 0


def solve1(lines):
    p = 1
    pairs = []
    for i in range(0, len(lines), 3):
        elem1 = eval(lines[i])
        elem2 = eval(lines[i + 1])
        c = compare(elem1, elem2)
        # if c == 0:
        #     print("OK")
        if c == 1:
            print(f"Pair {p}:")
            print(f"{elem1} <= {elem2} is {c}")
            print()
        if c > -1:
            pairs.append(p)
        p += 1
    print(pairs)
    print(sum(pairs))


def sort_lists(lists):
    return sorted(lists, key=functools.cmp_to_key(compare), reverse=True)


def solve2(lines):
    elems = []
    new_lines = [[[2]], [[6]]]
    elems.append(new_lines[0])
    elems.append(new_lines[1])
    positions = elems.index(new_lines[0]) + 1, elems.index(new_lines[1]) + 1
    for i in range(0, len(lines), 3):
        elem1 = eval(lines[i])
        elem2 = eval(lines[i + 1])
        elems.append(elem1)
        elems.append(elem2)
    elems = sort_lists(elems)
    positions = elems.index(new_lines[0]) + 1, elems.index(new_lines[1]) + 1
    print(elems)
    print(f"Positions: {positions}")
    print(positions[0] * positions[1])


if __name__ == "__main__":
    lines = read("input.txt")
    solve1(lines)
    solve2(lines)
