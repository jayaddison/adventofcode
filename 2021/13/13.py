content = open("13.txt").read()

coordinates = set()
max_x = 0
max_y = 0

pairs, instructions = content.split("\n\n")
for pair in pairs.split("\n"):
    x, y = pair.split(",")
    x, y = int(x), int(y)
    max_x, max_y = max(max_x, x), max(max_y, y)
    coordinates.add((x, y))

def print_coordinates():
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print("#" if (x, y) in coordinates else ".", end="")
        print()
    print()
    print(f"{len(coordinates)} dots")
    print()

def fold_vertical(f_y):
    global max_y
    for y in range(f_y, max_y + 1):
        for x in range(max_x + 1):
            if (x, y) not in coordinates:
                continue
            transposed_y = f_y - (y - f_y)
            coordinates.add((x, transposed_y))
            coordinates.remove((x, y))
    max_y = f_y - 1

def fold_horizontal(f_x):
    global max_x
    for y in range(max_y + 1):
        for x in range(f_x, max_x + 1):
            if (x, y) not in coordinates:
                continue
            transposed_x = f_x - (x - f_x)
            coordinates.add((transposed_x, y))
            coordinates.remove((x, y))
    max_x = f_x - 1

for instruction in instructions.split("\n"):
    instruction = instruction.strip()
    if not instruction:
        continue
    token = instruction.split(" ")[-1]
    axis, point = token.split("=")
    point = int(point)
    if axis == "y":
        fold_vertical(point)
    if axis == "x":
        fold_horizontal(point)
    print_coordinates()
