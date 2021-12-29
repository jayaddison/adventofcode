content = open("11.txt").read()

grid = []
for line in content.split("\n"):
    row = []
    for x, value in enumerate(line):
        energy = int(value)
        row.append(energy)
    if row:
        grid.append(row)


def get_neighbours(x, y):
    results = []
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            n_x = x + dx
            n_y = y + dy
            if n_x < 0 or n_y < 0:
                continue
            if n_x == x and n_y == y:
                continue
            try:
                grid[n_y][n_x]
                results.append((n_x, n_y))
            except:
                pass
    return results


has_flashed = set()

def increment(x, y):
    grid[y][x] += 1

def flash(x, y):
    if (x, y) in has_flashed:
        return
    has_flashed.add((x, y))
    for (n_x, n_y) in get_neighbours(x, y):
        increment(n_x, n_y)
        if grid[n_y][n_x] > 9 and (n_x, n_y) not in has_flashed:
            flash(n_x, n_y)

def step():
    has_flashed.clear()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            increment(x, y)
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] > 9 and (x, y) not in has_flashed:
                flash(x, y)
    for (x, y) in has_flashed:
        grid[y][x] = 0
    return len(has_flashed)

counter = 1
cell_count = len(grid) * len(grid[0])
while step() != cell_count:
    counter += 1
print(counter)
