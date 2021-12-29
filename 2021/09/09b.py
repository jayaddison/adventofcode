from heapq import heappush, nlargest
from functools import reduce
from operator import mul

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
                results.append((n_x, n_y, grid[n_y][n_x]))
            except:
                pass
    return results

def get_basin(x, y, level):
    basin = set()
    if x < 0 or y < 0:
        return basin
    try:
        height = grid[y][x]
    except:
        return basin
    if height == 9:
        return basin
    basin.add((x, y))
    for (n_x, n_y, neighbour) in get_neighbours(x, y):
        if neighbour > level:
            basin = basin | get_basin(n_x, n_y, neighbour)
    return basin

basin_sizes = []
for y in range(len(grid)):
    for x in range(len(grid[0])):
        height = grid[y][x]
        neighbours = get_neighbours(x, y)
        lowpoint = all(neighbour > height for (_, _, neighbour) in neighbours)
        if lowpoint:
            basin = get_basin(x, y, height)
            heappush(basin_sizes, len(basin))

largest_basins = (nlargest(3, basin_sizes))
print(reduce(mul, largest_basins, 1))
