from collections import defaultdict

content = open("05.txt").read()

supplies, operations = content.split("\n\n")


def parse_stacks(supplies):
    stacks = defaultdict(list)
    for line in supplies.splitlines():
        indices = {idx: char for idx, char in enumerate(line) if char.isupper()}
        for index, crate in indices.items():
           stacks[index].insert(0, crate)
        if not indices:
            numbers = {idx: char for idx, char in enumerate(line) if char.isdigit()}
            for index, number in numbers.items():
                stacks[number] = stacks.pop(index, [])
    return stacks

def move(from_stack, to_stack, item_count):
    items = []
    for _ in range(item_count):
        items.append(from_stack.pop())
    for _ in range(item_count):
        to_stack.append(items.pop())

stacks = parse_stacks(supplies)
for line in operations.splitlines():
    operation, _, arguments = line.partition(" from ")
    op_name, _, op_count = operation.partition(" ")
    from_stack, _, to_stack = arguments.partition(" to ")
    assert op_name == "move"
    move(stacks[from_stack], stacks[to_stack], int(op_count))

print("".join(stack.pop() if stack else "" for stack in stacks.values()))
