content = open("01.txt").read().splitlines()

total = 0
for line in content:
    numbers = [c for c in line if c.isdigit()]
    value = f"{numbers[0]}{numbers[-1]}"
    total += int(value)
print(total)
