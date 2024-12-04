import re
import sys

memory = sys.stdin.read()
multiplication_enabled = True
multiplication_accumulator = 0

findings = re.finditer(r"(do)\(\)|(don't)\(\)|(mul)\((\d{1,3}),(\d{1,3})\)", memory)
for finding in findings:
    filtered_groups = tuple(group for group in finding.groups() if group)
    instruction = filtered_groups[0]
    match instruction:
        case "do":
            multiplication_enabled = True
        case "don't":
            multiplication_enabled = False
        case "mul" if multiplication_enabled:
            arguments = map(int, filtered_groups[1:])
            product = int.__mul__(*arguments)
            multiplication_accumulator += product

print(multiplication_accumulator)
