from collections import Counter

content = open("01.txt").read().splitlines()

elf = 0
calories = Counter()
for line in content:
    if not line:
        elf += 1
        continue
    calories[elf] += int(line)

total_calories = 0
for _, calories in calories.most_common(3):
    total_calories += calories
print(total_calories)
