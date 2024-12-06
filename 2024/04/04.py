import sys

def generate_horizontals(grid):
    for row in grid:
        yield row

def generate_verticals(grid):
    for idx in range(len(grid[0])):
        yield (row[idx] for row in grid)

def generate_diagonals(grid):
    LEFT, RIGHT = 0, len(grid[0])
    TOP, BOTTOM = 0, len(grid)

    # commencing from the first row, down-rightwards
    for idx in range(RIGHT):
        idy, offset, value = 0, 0, ''
        while 0 <= idx + offset < RIGHT and 0 <= idy + offset < BOTTOM:
            value += grid[idy + offset][idx + offset]
            offset += 1
        yield value

    # commencing from the first row, down-leftwards
    for idx in range(RIGHT):
        idy, offset, value = 0, 0, ''
        while 0 <= idx - offset < RIGHT and 0 <= idy + offset < BOTTOM:
            value += grid[idy + offset][idx - offset]
            offset += 1
        yield value

    # commencing from the first column, down-rightwards
    for idy in range(1, BOTTOM):
        value = ''
        for offset, idx in enumerate(range(0, RIGHT - idy)):
            value += grid[idy + offset][idx]
        yield value

    # commencing from the last column, down-leftwards
    for idy in range(1, BOTTOM):
        value = ''
        for offset, idx in enumerate(range(RIGHT - 1, idy - 1, -1)):
            value += grid[idy + offset][idx]
        yield value

def generate_paths(grid):
    for generator in generate_horizontals, generate_verticals, generate_diagonals:
        for result in generator(grid):
            result = list(result)
            yield str().join(result)
            yield str().join(reversed(result))

grid = []
for row in sys.stdin.read().splitlines():
    grid.append(row)

found = 0
for path in generate_paths(grid):
    found += path.count('XMAS')
print(found)
