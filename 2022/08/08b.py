from collections import defaultdict

content = open("08.txt").read()

grid = []
for line in content.splitlines():
    grid.append([int(c) for c in list(line)])

scores = defaultdict(lambda: defaultdict(lambda: 1))
height, width = len(grid), len(grid[0])
for i in range(height):
    for j in range(width):
        for direction in (0, 1), (0, -1), (1, 0), (-1, 0):
            step_y, step_x = direction
            position_y, position_x = i + step_y, j + step_x
            altitude, score = grid[i][j], 0
            while 0 <= position_x < width and 0 <= position_y < height:
                score += 1
                if grid[position_y][position_x] >= altitude:
                    break
                position_x += step_x
                position_y += step_y
            scores[i][j] *= score


for i in range(0, len(grid)):
    for j in range(0, len(grid[i])):
        print(grid[i][j], end='')
    print()

for i in range(0, len(grid)):
    for j in range(0, len(grid[i])):
        print(f"  {scores[i][j]}  ", end='')
    print()
