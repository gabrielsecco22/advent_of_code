



def sum_nth_largest(numbers, nth):
    numbers.sort()
    print(numbers[-nth:])
    return sum(numbers[-nth:])


def read(filename):
    elves = []
    file = open(filename, "r")
    lines = file.read().split("\n")
    sum = 0
    for e in lines:
        if e:
            sum += int(e)
        else:
            elves.append(sum)
            sum = 0
    return elves


if __name__ == "__main__":
    elves_list = read("input.txt")
    print(sum_nth_largest(elves_list, 1))
    print(sum_nth_largest(elves_list, 3))
