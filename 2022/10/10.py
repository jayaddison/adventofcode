from collections import defaultdict

REGISTERS = {
    "X": 1,
}
CYCLES = {
    "addx": 2,
    "noop": 1,
}


content = open("10.txt").read()
instructions = content.splitlines()
pending_operations = defaultdict(list)
relevant_cycles = {20, 60, 100, 140, 180, 220}


cycle = 0
scan = -1
line = -1
while instructions or pending_operations:
    cycle += 1
    scan = (scan + 1) % 40
    line = (line + 1) % 6 if scan == 0 else (line)

    operations = pending_operations[cycle]
    for operation in operations:
        match operation.split():
            case "addx", v:
                REGISTERS["X"] += int(v)
    del pending_operations[cycle]

    if scan == 0:
        print()
    lit = abs(REGISTERS["X"] - scan) <= 1
    print('#' if lit else '.', end='')

    if pending_operations:
        continue

    instruction = instructions.pop(0)
    match instruction.split():
        case "addx", _:
            pending_operations[cycle + 2].append(instruction)
print()
