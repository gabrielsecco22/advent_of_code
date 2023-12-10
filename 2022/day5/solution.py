def read(filename):
    lines = open(filename).read().splitlines()
    return lines


def get_stacks(lines):
    """
       File input is a the current stacks of crates and the commands that needed to be done
           [D]
       [N] [C]
       [Z] [M] [P]
        1   2   3

       move 1 from 2 to 1
       move 3 from 1 to 3
       move 2 from 2 to 1
       move 1 from 1 to 2
       """
    # read the stacks
    num_stacks = (len(lines[0]) + 1) // 4
    levels = sum([1 for line in [x for x in lines if len(x) > 0 and x[1] != "1"] if line[0] == " " or line[0] == "["])

    stacks = [[] for _ in range(num_stacks)]

    for line in lines:
        if line[1] == "1":
            break
        new_stack = []
        # read 3 chars at a time
        for i in range(0, len(line), 4):
            crate = line[i:i + 3]
            # if the crate is not empty
            if crate != "   ":
                stacks[i // 4].append(crate)
    for s in stacks:
        s.reverse()
    return stacks


def get_commands(lines):
    levels = sum([1 for line in [x for x in lines if len(x) > 0 and x[1] != "1"] if line[0] == " " or line[0] == "["])
    commands = []
    for line in lines[levels + 2:]:
        # parse x,y,z from "move x from y to z"
        parts = line.split(" ")
        x, y, z = int(parts[1]), int(parts[3]), int(parts[5])
        commands.append((x, y, z))

    return commands


def solution1(lines, crates_at_once=1):
    commands = get_commands(lines)
    stacks = get_stacks(lines)

    for command in commands:
        stacks = move(stacks, command, crates_at_once)

    message = ""
    for stack in stacks:
        if len(stack) > 0:
            message += stack[-1][1]
    return message


def move(stacks, command, crates_at_once):
    x, y, z = command
    # move x crates from stack y to stack z
    moved = 0
    while moved < x:
        # remove creates_at_once from stack y until it reaches x
        buffer = min(crates_at_once, len(stacks[y - 1]), x)
        buffer_stack = []
        for _ in range(buffer):
            buffer_stack.append(stacks[y - 1].pop())
            moved += 1
        buffer_stack.reverse()
        stacks[z - 1].extend(buffer_stack)
    return stacks


lines = read("input.txt")
print(solution1(lines))
print(solution1(lines, 2000))
