class Tile:

    def __init__(self, elevation):
        self.elevation = elevation

    def calculate_reachable_tiles(self, surroundings):
        self.reachable_tiles = [
            step for step in surroundings
            if abs(step.elevation - self.elevation) <= 1
        ]

    def explore(self, path, destination, known_path=None):
        global tile_costs

        # Base case: we've reached the destination; return the entire path
        if self == destination:
            return [list(path) + [self]]

        # If we've taken a longer path to reach this tile than during a previous
        # attempt, then stop exploring this path
        if self in tile_costs and tile_costs[self] < len(path):
            return []

        # Avoid exploring paths that are longer than the best-found so far
        if known_path and len(path) >= len(known_path):
            return []

        # Avoid exploring the same tile repeatedly
        if self in path:
            return []

        tile_costs[self] = len(path)

        # Recursive case: explore paths for neighbouring reachable tiles
        paths = []
        for tile in self.reachable_tiles:
            for result in tile.explore(path=path | {self}, destination=destination, known_path=known_path):
                if result:
                    paths.append(result)
                    known_path = result
        return paths


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
    grid.append([Tile(elevation) for elevation in elevations])
    if start is not None:
        start_position = (i, start)
    if end is not None:
        end_position = (i, end)


# Connect each map tile to each of its reachable neighbours (creating a graph)
for i in range(len(grid)):
    for j in range(len(grid[i])):
        surroundings = []
        for step_y, step_x in (0, 1), (0, -1), (1, 0), (-1, 0):
            try:
                surroundings.append(grid[i + step_y][j + step_x])
            except IndexError:
                pass
        tile = grid[i][j]
        tile.calculate_reachable_tiles(surroundings)


# Explore the graph
tile_costs = dict()
(start_y, start_x), (end_y, end_x) = start_position, end_position
start, end = grid[start_y][start_x], grid[end_y][end_x]
paths = start.explore(path=set(), destination=end)
print([len(path) for path in paths])


assert (1, 5, [0, 0, 2, 3, 4, 25, 25]) == line_to_elevations("aScdeEz")
