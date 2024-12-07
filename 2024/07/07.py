import itertools
import sys

operators = {
    '*': int.__mul__,
    '+': int.__add__,
}

result = 0
for line in sys.stdin.read().splitlines():
    output, _, inputs = line.partition(': ')
    output, inputs = int(output), list(map(int, inputs.split()))
    procedures = itertools.product(operators.keys(), repeat=len(inputs) - 1)
    for procedure in procedures:
        evaluation = inputs[0]
        for input, operation in zip(inputs[1:], procedure):
            evaluation = operators[operation](evaluation, input)
        if evaluation == output:
            result += output
            break
print(result)
