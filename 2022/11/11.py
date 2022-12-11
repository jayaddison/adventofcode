from collections import Counter

content = open("11.txt").read().splitlines()


class Monkey:
    def __init__(self, items, operation, test, destination_true, destination_false):
        self.items = items
        self.operation = operation
        self.test = test
        match test.split():
            case "divisible", "by", value:
                self.test_operation = "divide"
                self.test_operand = int(value)
        self.destinations = {True: destination_true, False: destination_false}

    def __str__(self):
        return f"items: {self.items}"

    @property
    def holding_items(self):
        return bool(self.items)

    def inspect_item(self):
        item = self.items.pop(0)

        # apply operation to worry level
        parse_value = lambda x: item if x == "old" else int(x)
        match self.operation.split():
            case "*", value:
                item *= parse_value(value)
            case "+", value:
                item += parse_value(value)

        # test result of operation
        result = None
        if self.test_operation == "divide":
            result = item % self.test_operand == 0

        # append (throw) item to monkey at relevant destination
        monkeys[self.destinations[result]].items.append(item)


def parse_segment(segment):
    monkey_id, items, operation, test, destination_true, destination_false = segment[:6]
    monkey_id = int(monkey_id[7:-1])
    items = [int(item) for item in items[18:].split(", ")]
    operation = operation[23:]
    test = test[8:]
    destination_true = int(destination_true[29:])
    destination_false = int(destination_false[30:])
    return monkey_id, Monkey(items, operation, test, destination_true, destination_false)


monkeys = {}
while segment := content[:7]:
    monkey_id, monkey = parse_segment(segment)
    monkeys[monkey_id] = monkey
    content = content[7:]


monkey_activity = Counter()
for cycle in range(10000):
    for monkey_id, monkey in monkeys.items():
        while monkey.holding_items:
            monkey.inspect_item()
            monkey_activity[monkey_id] += 1

    for monkey in monkeys.values():
        print(monkey)
    print()

top_business_monkeys = monkey_activity.most_common(2)
top_monkey, second_monkey = top_business_monkeys
print(top_monkey[1] * second_monkey[1])

test_segment = (
    "Monkey 0:\n"
    "  Starting items: 79, 98\n"
    "  Operation: new = old * 19\n"
    "  Test: divisible by 23\n"
    "    If true: throw to monkey 2\n"
    "    If false: throw to monkey 3"
).splitlines()

parsed_segment = parse_segment(test_segment)
monkey_id, monkey = parsed_segment
assert (monkey_id, monkey.items, monkey.operation, monkey.test, monkey.destinations) == (
    0,
    [79, 98],
    "* 19",
    "divisible by 23",
    {True: 2, False: 3}
), parsed_segment
