def read(filename):
    lines = open(filename).read().splitlines()
    return lines


"""
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""
FORMS = [
    [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2), (3, 3)],
    [(2, 2), (2, 1), (0, 0), (1, 0), (2, 0), (3, 3)],
    [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
    [(0, 0), (1, 0), (0, 1), (1, 1), (2, 2)]
]

FORM_OFFSETS = [0, 2, 2, 3, 1]


class Piece:
    def __init__(self, formID, x, y):
        self.form = FORMS[formID][:-1]
        # self.x_offset = FORMS[formID][-1][0]
        # self.y_offset = FORMS[formID][-1][1]
        self.x = x
        self.y = y

    def position(self):
        return [(a + self.x, b + self.y) for a, b in self.form]

    def colision(self, other):
        return any(p in other.position() for p in self.position())

    def __repr__(self):
        return f"Piece({self.form}, {self.x}, {self.y})"

    def __str__(self):
        return str(self.position())


class Tetris:
    def __init__(self, width, moves):
        self.width = width
        self.grid = [[] for _ in range(width)]
        self.moving_pieces = []
        self.moves = moves
        self.curr_move = 0
        self.max_height = 0
        self.total_pieces = 0

    def settle(self, piece):
        for p in piece.position():
            self.grid[p[0]].append(p[1])
            self.max_height = max(self.max_height, p[1] + 1)

    def add(self, piece):
        self.moving_pieces.append(piece)
        self.total_pieces += 1

    def collision(self, piece, direction):
        if direction == "d":
            for p in piece.position():
                # print(p[0], end=" ")
                # print(f"Checking {p} for collision", direction, self.grid[p[0]])
                if (p[1] - 1) in self.grid[p[0]] or p[1] == 0:
                    return True
        elif direction == "l":
            for p in piece.position():
                # left wall or other piece
                if p[0] == 0:
                    return True
                if p[1] in self.grid[p[0] - 1]:
                    return True
        elif direction == "r":
            for p in piece.position():
                # right wall or other piece
                if p[0] == self.width - 1:
                    return True
                if p[1] in self.grid[p[0] + 1]:
                    return True
        return False

    # def collision_step(self):
    #     r = False
    #     for piece in self.moving_pieces:
    #         r = self.collision(piece, "d")
    #     return r

    def move_down_step(self):
        for piece in self.moving_pieces:
            if not self.collision(piece, "d"):
                piece.y -= 1
                print("Down Move", piece)
            else:
                self.settle(piece)
                self.moving_pieces.remove(piece)
                print("Down Collision - Settle")
        self.draw()
        print(f"Downward moves done")


    def move_lateral_step(self):
        if self.curr_move >= len(self.moves):
            print("No more moves")
            return
        for piece in self.moving_pieces:
            direction = "l" if self.moves[self.curr_move] == "<" else "r"
            if not self.collision(piece, direction):
                piece.x += 1 if direction == "r" else -1
                print(f"Lateral Move - {self.curr_move}", direction, self.moves[self.curr_move], piece)
            else:
                print(f"Lateral Collision - {self.curr_move}", direction, self.moves[self.curr_move], piece)

        self.draw()
        print(f"Move {self.curr_move} - {self.moves[self.curr_move]} done")
        print(f"Moves so far: {self.moves[:self.curr_move+1]}")
        self.curr_move += 1

    def step(self):
        while self.moving_pieces:
            # self.draw()
            # print(end="\n"*2)
            self.move_lateral_step()
            self.move_down_step()
            # self.collision_step()

    def draw(self):
        print(f"Draw {self.max_height + 8} lines")
        for i in range(self.max_height + 8, -1, -1):
            for j in range(self.width):
                if i in self.grid[j]:
                    print("#", end="")
                elif any((j, i) in p.position() for p in self.moving_pieces):
                    print("@", end="")
                else:
                    print(".", end="")
            print()
        print(f"Max height: {self.max_height}, Total pieces: {self.total_pieces}")



if __name__ == "__main__":
    moves = read("test_input.txt")[0]

    t = Tetris(width=7, moves=moves)
    num_pieces = len(FORMS)
    count = 0
    while True:
        # print(f"Adding piece {count} at height {t.max_height} + {FORM_OFFSETS[count % num_pieces]} + {3} = {t.max_height + FORM_OFFSETS[count % num_pieces] + 3}")
        # t.add(Piece(count % num_pieces, 2, t.max_height + FORM_OFFSETS[count % num_pieces] + 3))
        # print(f"Adding piece {count} at height {t.max_height} + {3} = {t.max_height + 3}")
        t.add(Piece(count % num_pieces, 2, t.max_height + 3))
        t.step()
        count += 1
        if count == 2022:
            break
    t.draw()
    print(t.max_height)

