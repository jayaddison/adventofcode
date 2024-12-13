import sys

grid = []
for line in sys.stdin.read().splitlines():
    grid.append([int(char) for char in line])

def neighbours(y, x):
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if abs(i) + abs(j) != 1:
                continue
            if y + i < 0 or x + j < 0:
                continue
            try:
                yield (y + i, x + j), grid[y + i][x + j]
            except IndexError:
                continue

def explore_trails(y, x, path=None):
    current = grid[y][x]
    if current == 9 and len(path) == 10:
        yield path
    for step, value in neighbours(y, x):
        if value == current + 1:
            yield from explore_trails(*step, path + [step])

results = []
for idy, row in enumerate(grid):
    for idx, value in enumerate(row):
        if value == 0:
            trails = list(explore_trails(idy, idx, path=[(idy, idx)]))
            destinations = set(trail[-1] for trail in trails)
            results.append(len(destinations))
print(sum(results))
