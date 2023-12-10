def read(filename):
    file = open(filename, "r")
    return file.read().split("\n")


# Rock, Paper, Scissors
def rps(p1, p2):
    CHOICE_POINTS = [1, 2, 3]
    RESULT_POINTS = [0, 3, 6]  # 0 lose, 3 tie, 6 win
    return CHOICE_POINTS[p1] + RESULT_POINTS[(p1 - p2 + 1) % 3], CHOICE_POINTS[p2] + RESULT_POINTS[(p2 - p1 + 1) % 3]


def test_rps():
    assert rps(0, 0) == (4, 4)
    assert rps(0, 1) == (1, 8)
    assert rps(0, 2) == (7, 3)
    assert rps(1, 0) == (8, 1)
    assert rps(1, 1) == (5, 5)
    assert rps(1, 2) == (2, 9)
    assert rps(2, 0) == (3, 7)
    assert rps(2, 1) == (9, 2)
    assert rps(2, 2) == (6, 6)



def apply_strategy1():
    map_letters = {"A": 0, "B": 1, "C": 2, "X": 0, "Y": 1, "Z": 2}
    points = 0
    for line in read("input.txt"):
        if line:
            c1, c2 = line.split(" ")
            points += rps(map_letters[c1], map_letters[c2])[1]
    return points

def apply_strategy2():
    map_letters = {"A": 0, "B": 1, "C": 2}
    # X - lose, Y - tie, Z - win
    response_letters = {"X": [2, 0, 1], "Y": [0, 1, 2], "Z": [1, 2, 0]}
    points = 0
    for line in read("input.txt"):
        if line:
            c1, c2 = line.split(" ")
            points += rps(map_letters[c1], response_letters[c2][map_letters[c1]])[1]
    return points


if __name__ == "__main__":
    test_rps()
    print("Strat 1 -", apply_strategy1())
    print("Strat 2 -", apply_strategy2())


