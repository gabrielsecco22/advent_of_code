class KeepAway:
    def __init__(self, monkeys, relief_decay=3):
        self.monkeys = monkeys
        for m in self.monkeys:
            m.relief_decay = relief_decay

    def get_monkey(self, monkey_id):
        return self.monkeys[monkey_id]

    def get_monkey_business(self):
        self.monkeys.sort(key=lambda monkey: monkey.num_inspected, reverse=True)
        return self.monkeys[0].num_inspected * self.monkeys[1].num_inspected

    def turn(self):
        for monkey in self.monkeys:
            monkey.play(self)

    def play(self, turns):
        for turn in range(turns):
            self.turn()


class Monkey:
    """
    Parse the following message into class attributes
    Monkey 0:
    Starting items: 79, 98
    Operation: new = old * 19
    Test: divisible by 23
        If true: throw to monkey 2
        If false: throw to monkey 3
    """

    def __init__(self, lines):
        self.monkey_id = int(lines[0].split(" ")[1][:-1])
        self.starting_items = [int(x) for x in lines[1].split(": ")[1].split(", ")]
        self.operation = lines[2].split("= ")[1]
        # (divisor, throw to monkey if true, throw to monkey if false)
        self.test = (int(lines[3].split("by ")[1]), int(lines[4].split(" ")[-1]), int(lines[5].split(" ")[-1]))
        self.num_inspected = 0
        self.relief_decay = 3

    def __repr__(self):
        return f"Monkey {self.monkey_id}: {self.starting_items}: inspected {self.num_inspected} items"

    def operate(self, old):
        # parse the operation expression: new = old * 19
        return eval(self.operation)

    def inspect(self):
        self.starting_items = [self.operate(x) for x in self.starting_items]
        self.num_inspected += len(self.starting_items)

    def before_test(self):
        # sol 2 - mod the product of test divisors
        self.starting_items = [x % 9699690 for x in self.starting_items]
        # sol 1 - divide by 3
        # self.starting_items = [x//3 for x in self.starting_items]

    def test_throws(self):
        throws = []
        for item in self.starting_items:
            if item % self.test[0] == 0:
                throws.append((item, self.test[1]))
            else:
                throws.append((item, self.test[2]))
        return throws

    def throw(self, game: KeepAway):
        throws = self.test_throws()
        for item, monkey_id in throws:
            # append to target monkey's starting items
            game.get_monkey(monkey_id).starting_items.append(item)
            # remove from self starting items
            self.starting_items.remove(item)

    # monkey's turn order: inspects, before_test, test, throw
    def play(self, game: KeepAway):
        self.inspect()
        self.before_test()
        self.throw(game)






def read(filename):
    lines = open(filename).read().splitlines()
    return lines


if __name__ == "__main__":
    lines = read("input.txt")
    monkeys = []
    for i in range(0, len(lines), 7):
        monkeys.append(Monkey(lines[i:i+7]))
    x = 1
    for m in monkeys:
        x = x * m.test[0]
        print(f"x * {m.test[0]}")
    print(x)
    game = KeepAway(monkeys, relief_decay=1)
    game.play(10000)
    print(game.monkeys)
    print(game.get_monkey_business())



    # print(monkeys[0])
    # print(monkeys[0].operate(5))
    # print(monkeys[1].operate(5))






