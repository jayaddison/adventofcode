content = open("03.txt").read()

part_grid = {}
symbol_grid = {}

# Find potential part numbers and symbols in the grid
for y, line in enumerate(content.splitlines()):
    part_number = ""
    part_grid[y] = {}
    symbol_grid[y] = {}
    for x, char in enumerate(line):
        if char.isdigit():
            part_number += char
        else:
            if char == "*":
                symbol_grid[y][x] = []
            if part_number:
                part_grid[y][x - len(part_number)] = part_number
                part_number = ""
    if part_number:
        part_grid[y][x - len(part_number)] = part_number
        part_number = ""

# Filter the part numbers to cases where a symbol is adjacent
filtered_grid = {}
for y, part_map in part_grid.items():
    for x, part_number in part_map.items():
        for yoffset in (-1, 0, 1):
            for xoffset in range(-1, len(part_number) + 1):
                try:
                    symbol_grid[y + yoffset][x + xoffset].append(int(part_number))
                    if y not in filtered_grid:
                        filtered_grid[y] = {}
                    filtered_grid[y][x] = part_number
                except:
                    pass

# Sum the filtered part numbers
total = 0
for y, part_map in symbol_grid.items():
    for x, part_numbers in part_map.items():
        if len(part_numbers) == 2:
            total += (part_numbers[0] * part_numbers[1])
print(total)
