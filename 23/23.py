from copy import deepcopy

content = open("23.txt").read()
lines = content.split("\n")

MOVEMENT_COSTS = {"A": 1, "B": 10, "C": 100, "D": 1000}
DESTINATION_COLUMNS = {"A": 3, "B": 5, "C": 7, "D": 9}
HALLWAY_ROW = 1


class World:
    def __init__(self, lines):
        self.grid = []
        self.amphipods = {}
        for y, line in enumerate(lines):
            row = []
            for x, char in enumerate(line):
                row.append(char not in ("#", " "))
                if char.isalpha():
                    Amphipod(self, char, x, y)
            if row:
                self.grid.append(row)

    def __str__(self):
        result = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                content = self.amphipods.get((x, y))
                content = content or "." if self.grid[y][x] else "#"
                result.append(str(content))
            result.append("\n")
        return str().join(result)

    def __add__(self, amphipod):
        self.amphipods[(amphipod.x, amphipod.y)] = amphipod
        return self

    def passable(self, x, y):
        if not self.grid[y][x]:
            return False
        if (x, y) in self.amphipods:
            return False
        return True

    def stoppable(self, x, y):
        if not self.passable(x, y):
            return False
        if y == HALLWAY_ROW and x in DESTINATION_COLUMNS.values():
            return False
        return True

    @property
    def complete(self):
        return all([amphipod.in_position for amphipod in self.amphipods.values()])


class Amphipod:
    def __init__(self, world, value, x, y):
        self.world = world
        self.value = value
        self.x = x
        self.y = y
        self.world += self

    def __str__(self):
        return self.value

    def _directional_step(self, origin, destination):
        return int((destination - origin) / abs((destination - origin) or 1))

    def path(self, destination_x, destination_y):
        origin_x, origin_y = self.x, self.y
        while origin_x != destination_x or origin_y != destination_y:
            step_x = self._directional_step(origin_x, destination_x)
            if step_x and self.world.passable(origin_x + step_x, origin_y):
                origin_x += step_x
                yield origin_x, origin_y
                continue
            step_y = self._directional_step(origin_y, destination_y)
            if step_y and self.world.passable(origin_x, origin_y + step_y):
                origin_y += step_y
                yield origin_x, origin_y
                continue
            if step_x and not self.world.passable(origin_x + step_x, origin_y):
                raise Exception("Unable to reach destination; blocked")
            if step_y and not self.world.passable(origin_x, origin_y + step_y):
                raise Exception("Unable to reach destination; blocked")

    def path_distance(self, destination_x, destination_y):
        steps = 0
        for _ in self.path(destination_x, destination_y):
            steps += 1
        return steps

    def move(self, destination_x, destination_y):
        try:
            steps = self.path_distance(destination_x, destination_y)
        except:
            raise
        self.world.amphipods.pop((self.x, self.y))
        self.x, self.y = destination_x, destination_y
        self.world.amphipods[(self.x, self.y)] = self
        return self.movement_cost * steps

    @property
    def movement_cost(self):
        return MOVEMENT_COSTS[self.value]

    @property
    def destination_column(self):
        return DESTINATION_COLUMNS[self.value]

    @property
    def in_hallway(self):
        return self.y == HALLWAY_ROW

    @property
    def in_position(self):
        return self.x == self.destination_column

    def possible_moves(self):
        results = []
        if all(
            [
                amphipod.in_position
                for amphipod in self.world.amphipods.values()
                if amphipod.x == self.x
            ]
        ):
            return results

        if self.in_hallway:
            x = self.destination_column
            if any(
                [
                    not amphipod.in_position
                    for amphipod in self.world.amphipods.values()
                    if amphipod.x == x
                ]
            ):
                return results
            for y, _ in enumerate(self.world.grid):
                if y == HALLWAY_ROW:
                    continue
                if self.world.stoppable(x, y) and not self.world.stoppable(x, y + 1):
                    results.append((x, y))
                    break

        else:
            if self.world.passable(self.x, self.y - 1):
                for x, _ in enumerate(self.world.grid[HALLWAY_ROW]):
                    if self.world.stoppable(x, HALLWAY_ROW):
                        results.append((x, HALLWAY_ROW))

        reachable_results = []
        for result in results:
            try:
                self.path_distance(*result)
                reachable_results.append(result)
            except:
                continue
        return sorted(reachable_results, key=lambda p: self.path_distance(*p))


test_world = World(
    lines=[
        "#############",
        "#...........#",
        "###.#.#.#.###",
        "  #.#.#.#.#  ",
        "  #########  ",
    ]
)
assert test_world.passable(1, 1)
assert test_world.stoppable(1, 1)
assert not test_world.passable(0, 1)
assert test_world.passable(3, 2)
assert not test_world.passable(4, 2)

test_amphipod = Amphipod(world=test_world, value="A", x=5, y=3)
test_world += test_amphipod

assert test_amphipod.path_distance(4, 1) == 3
assert not test_amphipod.in_hallway
assert not test_world.passable(5, 3)

test_amphipod.move(2, 1)
assert test_world.passable(5, 3)
assert not test_world.passable(2, 1)


def explore(original_world, path, path_cost):
    for amphipod in original_world.amphipods.values():
        original_amphipod = amphipod
        for move in amphipod.possible_moves():
            amphipod = deepcopy(original_amphipod)
            move_cost = amphipod.move(*move)
            explore_path = tuple(list(path) + [(amphipod.value, move)])
            explore_cost = path_cost + move_cost

            if min_path_cost and explore_cost >= min_path_cost:
                continue

            if amphipod.world.complete:
                yield explore_path, explore_cost
                continue
            yield from explore(amphipod.world, explore_path, explore_cost)


world = World(lines)
min_path, min_path_cost = None, None
for path, cost in explore(world, tuple(), 0):
    if min_path_cost is None or cost < min_path_cost:
        min_path_cost = cost
        min_path = path
    print(f"{cost} : {path}")
