content = open("15.txt").read()

matrix = []
for line in content.split("\n"):
    line = line.strip()
    if not line:
        continue
    matrix.append([int(char) for char in line])

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

grid = Grid(matrix=matrix)
origin = grid.node(0, 0)
destination = grid.node(grid.width - 1, grid.height - 1)
finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
path, _ = finder.find_path(origin, destination, grid)
cost = sum(matrix[y][x] for (x, y) in path[1:])

for y in range(len(matrix)):
    for x in range(len(matrix[0])):
        print("." if (x, y) in path else matrix[y][x], end="")
    print()
print()
print(cost)
