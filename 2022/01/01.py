from collections import Counter

content = open("01.txt").read().splitlines()

elf = 0
calories = Counter()
for line in content:
    if not line:
        elf += 1
        continue
    calories[elf] += int(line)

for _, max_calories in calories.most_common(1):
    print(max_calories)
