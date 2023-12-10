from collections import deque

# The jet pattern and the rock shapes
jet_pattern = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>'
rocks = [
    ['####'],
    ['.#.', '###', '.#.'],
    ['..#', '..#', '###'],
    ['#', '#', '#', '#'],
    ['##', '##'],
]

# Function to check if a rock can be moved in a particular direction
def can_move(rock, stopped_rocks, direction):
    for i, row in enumerate(rock):
        for j, cell in enumerate(row):
            if cell == '@':
                if (
                    j + direction < 0 or
                    j + direction >= 7 or
                    (i + 1 < len(rock) and rock[i+1][j+direction] == '.') or
                    (i + 1 == len(rock) and (j + direction, i) in stopped_rocks)
                ):
                    return False
    return True

# Function to move a rock in a particular direction
def move_rock(rock, direction):
    new_rock = []
    for row in rock:
        new_row = []
        for j, cell in enumerate(row):
            if cell == '@':
                new_row.append('.')
                new_row.append('@' if j+direction < 0 or j+direction >= 7 else row[j+direction])
            else:
                new_row.append(cell)
        new_rock.append(''.join(new_row))
    return new_rock

# Initialize the stopped rocks and the queue of falling rocks
stopped_rocks = set()
falling_rocks = deque([(rock, 3) for rock in rocks])

# Initialize the grid
grid = [['.' for _ in range(7)] for _ in range(10)]

# Process the falling rocks
for i in range(10):
    # Get the next rock shape and the direction it should be moved
    rock_idx = i % len(rocks)
    rock_shape = rocks[rock_idx]
    direction = 1 if jet_pattern[i % len(jet_pattern)] == '>' else -1

    # Move the falling rocks
    while falling_rocks:
        rock, y = falling_rocks.popleft()
        if can_move(rock, stopped_rocks, direction):
            rock = move_rock(rock, direction)
            y -= 1
            falling_rocks.append((rock, y))
        else:
            for j, row in enumerate(rock):
                for k, cell in enumerate(row):
                    if cell == '@':
                        stopped_rocks.add((k+direction, y+j-1))
                        grid[y+j-1][k+direction] = '#'
            break

    # Add a new rock to the queue
    if i % len(rocks) == 0:
        falling_rocks.append((rock_shape, 9))

    # Print the grid
    for row in grid:
        print(''.join(row))
    print('+-------+')