def read(filename):
    lines = open(filename).read().splitlines()
    return lines

def addx(x, y):
    return x + y


OP_CODES = {
    "addx":{
        "f": addx,
        "cicles": 2
    },
    "noop":{
        "f": None,
        "cicles": 1
    },
}


class Computer:
    def __init__(self):
        self.registers = [1]
        self.cicles = 0
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    def run(self, program):
        for instruction in program:
            op = OP_CODES[instruction["op"]]
            op_f = op["f"]
            for c in range(op["cicles"]):
                self.cicles += 1
                self.notify()
            if op_f is not None:
                args = instruction["args"], self.registers[0]
                self.registers[0] = op_f(*args)



class ComputerObserver:
    def __init__(self, observed_cicles):
        self.observed_cicles = observed_cicles
        self.observed_values = []

    def update(self, subject):
        if subject.cicles in self.observed_cicles:
            sig_str = subject.cicles * subject.registers[0]
            print(f"Computer cicles: {subject.cicles}: {subject.registers[0]}. Signal Strength: {sig_str}")
            self.observed_values.append(sig_str)

    def summary(self):
        return f"{self.__repr__()} {sum(self.observed_values)}"


class CRT:
    def __init__(self, sprite, width, height):
        self.sprite = sprite
        self.screen = []
        self.width = width
        self.height = height

    def update(self, subject):
        char = "."
        pixel_pos = subject.cicles % self.width - 1
        if abs(subject.registers[0] - pixel_pos) < 2:
            char = "#"
        self.screen.append(char)

    def draw(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.screen[i * self.width + j], end="")
            print()




    def summary(self):
        return f"{self.__repr__()} {sum(self.observed_values)}"



if __name__ == "__main__":
    # program = [
    #     {"op": "noop", "args": None},
    #     {"op": "addx", "args": 1},
    #     {"op": "noop", "args": None},
    # ]
    lines = read("input.txt")
    program = []
    for line in lines:
        if line.startswith("noop"):
            program.append({"op": "noop", "args": None})
        else:
            op, arg = line.split(" ")
            program.append({"op": op, "args": int(arg)})
    computer = Computer()
    observed_cicles = [20, 60, 100, 140, 180, 220]
    observer = ComputerObserver(observed_cicles)
    crt = CRT("###", 40, 6)
    computer.attach(observer)
    computer.attach(crt)
    computer.run(program)
    print(f"Registers: {computer.registers}")
    print(f"Cicles: {computer.cicles}")
    print(observer.summary())
    crt.draw() # PGPHBEAB
