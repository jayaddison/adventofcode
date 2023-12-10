content = open("04.txt").read()

score = 0
for line in content.splitlines():
    _, _, numbers = line.partition(": ")
    winning_numbers, _, found_numbers = numbers.partition(" | ")
    winning_numbers = set(filter(None, winning_numbers.split(" ")))
    found_numbers = set(filter(None, found_numbers.split(" ")))
    matched = len(winning_numbers & found_numbers)
    if matched:
        score += 2 ** (matched - 1)
print(score)
