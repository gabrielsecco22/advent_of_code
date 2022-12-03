def get_priority(char):
    """
    Map a-z to 1-26
    Map A-Z to 27-52

    """
    if char.islower():
        return ord(char) - 96
    else:
        return ord(char) - 38


def split_line(line):
    return line[0:len(line) // 2], line[len(line) // 2:]


def binary_search(char, sorted_char_list):
    """
    :param char:
    :param sorted_char_list: sorted list of chars
    :return: index of char in sorted_char_list
    """
    def bs_rec(char, start, end, sorted_char_list):
        if start > end:
            return -1
        mid = (start + end) // 2
        if sorted_char_list[mid] == char:
            return mid
        elif sorted_char_list[mid] < char:
            return bs_rec(char, mid + 1, end, sorted_char_list)
        else:
            return bs_rec(char, start, mid - 1, sorted_char_list)

    return bs_rec(char, 0, len(sorted_char_list) - 1, sorted_char_list)


def read(filename):
    lines = open(filename).read().splitlines()
    return lines


def solution1(lines):
    sum = 0
    for line in lines:
        r1, r2 = split_line(line)
        r1 = sorted(r1)
        r2 = sorted(r2)
        found = False
        last_char = ""
        for r1_char in r1:
            if r1_char == last_char:
                continue
            char_pos = binary_search(r1_char, r2)
            if char_pos != -1:
                found = True
                sum += get_priority(r1_char)
            if found:
                break
    return sum


def solution2(lines):
    sum = 0
    # groups of 3 lines
    for i in range(0, len(lines), 3):
        r1, r2, r3 = lines[i:i + 3]
        r1 = sorted(r1)
        r2 = sorted(r2)
        r3 = sorted(r3)
        found = False
        last_char = ""
        for r1_char in r1:
            if r1_char == last_char:
                continue
            char_pos = binary_search(r1_char, r2)
            if char_pos != -1:
                char_pos = binary_search(r1_char, r3)
                if char_pos != -1:
                    found = True
                    sum += get_priority(r1_char)
            if found:
                break
    return sum


if __name__ == '__main__':
    test_get_priority()
    test_split_line()
    test_binary_search()
    test_solution1()
    test_solution2()
    lines = read('input.txt')
    print(solution1(lines))
    print(solution2(lines))

