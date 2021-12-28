from random import sample


def generate_inputs():
    possible_digits = [str(x) for x in range(1, 10, 1)]
    while True:
        yield str().join(sample(possible_digits, counts=[2] * 9, k=14))


def read_line():
    return input()


def yield_characters(line):
    yield from line


class Argument:
    def read(self):
        pass

    def write(self, value):
        pass


class LiteralArgument(Argument):
    def __init__(self, value):
        self.value = int(value)

    def read(self):
        return self.value

    def write(self, value):
        raise Exception("Cannot write to literal argument")


class VariableArgument(Argument):
    def __init__(self, alu, variable_name):
        self.alu = alu
        self.variable_name = variable_name

    def read(self):
        return self.alu.variables[self.variable_name]

    def write(self, value):
        self.alu.variables[self.variable_name] = value


class Instruction:
    pass


class Input(Instruction):
    def __init__(self, destination: VariableArgument):
        result = int(next(destination.alu.input_stream))
        destination.write(result)


class Add(Instruction):
    def __init__(self, left: Argument, right: Argument):
        result = left.read() + right.read()
        left.write(result)


class Mul(Instruction):
    def __init__(self, left: Argument, right: Argument):
        result = left.read() * right.read()
        left.write(result)


class Div(Instruction):
    def __init__(self, left: Argument, right: Argument):
        result = int(left.read() / right.read())
        left.write(result)


class Mod(Instruction):
    def __init__(self, left: Argument, right: Argument):
        result = left.read() % right.read()
        left.write(result)


class Eql(Instruction):
    def __init__(self, left: Argument, right: Argument):
        result = 1 if left.read() == right.read() else 0
        left.write(result)


class ALU:

    INSTRUCTION_NAMES = {
        "inp": Input,
        "add": Add,
        "mul": Mul,
        "div": Div,
        "mod": Mod,
        "eql": Eql,
    }

    def __init__(self, input_stream):
        self.variables = {
            "w": 0,
            "x": 0,
            "y": 0,
            "z": 0,
        }
        self.input_stream = input_stream

    def __str__(self):
        variables = [f"{name}={value}" for name, value in self.variables.items()]
        return " ".join(variables)

    def process(self, instruction):
        instruction_name, argument_list = instruction.split(maxsplit=1)
        arguments = [
            VariableArgument(self, argument)
            if argument.isalpha()
            else LiteralArgument(argument)
            for argument in argument_list.split()
        ]
        self.INSTRUCTION_NAMES[instruction_name](*arguments)


program = open("24.txt").read()

noops = set()
min_z, min_input = None, None
for input in generate_inputs():
    alu = ALU(input_stream=yield_characters(input))
    for n, instruction in enumerate(program.split("\n")):
        if not instruction:
            continue
        alu.process(instruction)
        prev_alu = str(alu)
        z = alu.variables["z"]
    if min_z is None or z < min_z:
        min_z = z
        min_input = input
    print(input)
    print(f"{min_input} ({min_z})")
