def read(filename):
    lines = open(filename).read().splitlines()
    return lines


def is_sub_range(sub_range, super_range):
    sub_start, sub_end = sub_range
    super_start, super_end = super_range
    return sub_start >= super_start and sub_end <= super_end


def is_range_overlap(range1, range2):
    start1, end1 = range1
    start2, end2 = range2
    return start1 <= end2 and start2 <= end1


def solution1(lines):
    sum = 0
    for line in lines:
        range1, range2 = line.split(",")
        range1 = tuple(int(item) for item in range1.split("-"))
        range2 = tuple(int(item) for item in range2.split("-"))
        if is_sub_range(range1, range2) or is_sub_range(range2, range1):
            sum += 1
    return sum


def solution2(lines):
    # find lines with overlap
    sum = 0
    for line in lines:
        range1, range2 = line.split(",")
        range1 = tuple(int(item) for item in range1.split("-"))
        range2 = tuple(int(item) for item in range2.split("-"))
        if is_range_overlap(range1, range2):
            sum += 1
    return sum


if __name__ == "__main__":
    lines = read("input.txt")
    print(solution1(lines))
    print(solution2(lines))

