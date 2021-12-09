content = open("09.txt").read()

grid = []
for line in content.split("\n"):
    row = []
    for x, value in enumerate(line):
        height = int(value)
        row.append(height)
    if row:
        grid.append(row)

def get_neighbours(x, y):
    results = []
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if abs(dx) and abs(dy):
                continue
            n_x = x + dx
            n_y = y + dy
            if n_x < 0 or n_y < 0:
                continue
            if n_x == x and n_y == y:
                continue
            try:
                results.append(grid[n_y][n_x])
            except:
                pass
    return results

total_risk = 0
for y in range(len(grid)):
    for x in range(len(grid[0])):
        height = grid[y][x]
        neighbours = get_neighbours(x, y)
        lowpoint = all(neighbour > height for neighbour in neighbours)
        risk = (height + 1) if lowpoint else 0
        total_risk += risk

print(total_risk)
