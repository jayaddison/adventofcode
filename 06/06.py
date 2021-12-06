line = open("06.txt").read()

generation = {key: 0 for key in range(9)}
for age in line.split(","):
    generation[int(age)] += 1

LIMIT = 80

for day in range(LIMIT):
    next_generation = {key: 0 for key in range(9)}
    for key, count in generation.items():
        if count == 0:
            continue
        if key == 0:
            next_generation[6] = count
            next_generation[8] += count
        else:
            next_generation[key - 1] += count
    generation = next_generation

print(sum(count for count in generation.values()))
