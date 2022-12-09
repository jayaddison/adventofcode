content = open("08.txt").read()

grid = []
for line in content.splitlines():
    grid.append([int(c) for c in list(line)])


def trace_visibility(grid, start, end):
    x_start, y_start = start
    x_end, y_end = end

    x_step = (x_end - x_start)
    x_step = int(x_step / abs(x_step)) if x_step else 0

    y_step = (y_end - y_start)
    y_step = int(y_step / abs(y_step)) if y_step else 0

    peak = -1
    position = start
    while position != end:
        x, y = position
        if grid[y][x] > peak:
            visible.add((y, x))
        peak = max(peak, grid[y][x])
        position = (x + int(x_step), y + int(y_step))

visible = set()
width, height = len(grid[0]), len(grid)
for i in range(height):
    trace_visibility(grid, (0, i), (width - 1, i))
    trace_visibility(grid, (width - 1, i), (0, i))
for j in range(width):
    trace_visibility(grid, (j, 0), (j, height - 1))
    trace_visibility(grid, (j, height - 1), (j, 0))

for i in range(0, len(grid)):
    for j in range(0, len(grid[i])):
        print("." if (i, j) in visible else "#", end='')
    print()
print(len(visible))
