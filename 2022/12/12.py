def line_to_elevations(line):
    start, end, elevations = None, None, []
    for j, char in enumerate(line):
        start, char = (j, "a") if char == "S" else (start, char)
        end, char = (j, "z") if char == "E" else (end, char)
        elevations.append(ord(char) - ord("a"))
    return start, end, elevations


# Create a grid of map tiles
grid = []
content = open("12.txt").read()
for i, line in enumerate(content.splitlines()):
    start, end, elevations = line_to_elevations(line)
    grid.append([elevation for elevation in elevations])
    if start is not None:
        start_position = (i, start)
    if end is not None:
        end_position = (i, end)


# Explore the graph
(start_y, start_x), (end_y, end_x) = start_position, end_position

from pathfinding.core.grid import Grid
from pathfinding.finder.breadth_first import BreadthFirstFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

class TileGrid(Grid):
    def neighbors(self, node, diagonal_movement=DiagonalMovement.never):
        elevation = grid[node.y][node.x]
        for neighbour in super().neighbors(node, diagonal_movement):
            if grid[neighbour.y][neighbour.x] <= elevation + 1:
                yield neighbour

    def walkable(self, x, y):
        return super().inside(x, y)

origins = []
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] == 0:  # potential starting location
            origins.append((i, j))

best_path = []
for origin in origins:
    start_y, start_x = origin
    tile_grid = TileGrid(matrix=grid)
    origin = tile_grid.node(start_x, start_y)
    destination = tile_grid.node(end_x, end_y)
    finder = BreadthFirstFinder(diagonal_movement=DiagonalMovement.never)
    path, _ = finder.find_path(origin, destination, tile_grid)
    if path:
        if not best_path or len(path) < len(best_path):
            best_path = path
print(best_path)
print(len(best_path) - 1)


# Extremely hacky map printout
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if (j, i) == (start_x, start_y):
            print('S', end='')
        elif (j, i) == (end_x, end_y):
            print('E', end='')
        elif (j, i) in path:
            print('@', end='')
        else:
            print(str(grid[i][j])[0], end='')
    print()


assert (1, 5, [0, 0, 2, 3, 4, 25, 25]) == line_to_elevations("aScdeEz")
