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
from pathfinding.finder.dijkstra import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

class TileGrid(Grid):
    def neighbors(self, node, diagonal_movement=DiagonalMovement.never):
        neighbours = super().neighbors(node, diagonal_movement)
        elevation = grid[node.y][node.x]
        for neighbour in neighbours:
            if grid[neighbour.y][neighbour.x] <= elevation + 1:
                yield neighbour

    def walkable(self, x, y):
        return super().inside(x, y)


tile_grid = TileGrid(matrix=grid)
origin = tile_grid.node(start_x, start_y)
destination = tile_grid.node(end_x, end_y)
finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
path, _ = finder.find_path(origin, destination, tile_grid)
print(path)
print(len(path))


assert (1, 5, [0, 0, 2, 3, 4, 25, 25]) == line_to_elevations("aScdeEz")
