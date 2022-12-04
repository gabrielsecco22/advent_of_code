#################################################
#       Rock          Paper           Scissors
#       A - 1         B - 2            C - 3
#################################################
# X : LOSE
#       C               A               B
# Y : DRAW
#       A               B               C
# Z : WIN
#       B               C               A
decrypting = {
    "X": {
        "X": 0,
        "A": 3,
        "B": 1,
        "C": 2
        },
    "Y": {
        "Y": 3,
        "A": 1,
        "B": 2,
        "C": 3
    },
    "Z": {
        "Z": 6,
        "A": 2,
        "B": 3,
        "C": 1
        }
}


points = 0
with open('input.txt') as f:
    for line in f.readlines():
        # Points for my play
        points += decrypting[line[2]][line[0]]
        points += decrypting[line[2]][line[2]]

    print(points)
