from collections import deque
from copy import deepcopy

content = open("23b.txt").read()
lines = content.split("\n")

MOVEMENT_COSTS = {"A": 1, "B": 10, "C": 100, "D": 1000}
DESTINATION_COLUMNS = {"A": 3, "B": 5, "C": 7, "D": 9}
HALLWAY_ROW = 1
HALLWAY_COLUMNS = [1, 11, 2, 10, 4, 8, 6]
ROOM_ROWS = [2, 3, 4, 5]


class World:
    def __init__(self, lines):
        self.amphipods = {}
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char.isalpha():
                    Amphipod(self, char, x, y)

    def __str__(self):
        result = []
        for y in range(1, 6):
            for x in range(1, 12):
                content = self.amphipods.get((x, y))
                content = content or "."
                result.append(str(content))
            result.append("\n")
        return str().join(result)

    def __add__(self, amphipod):
        self.amphipods[(amphipod.x, amphipod.y)] = amphipod
        return self

    def occupied(self, x, y):
        return (x, y) in self.amphipods

    @property
    def complete(self):
        return all([amphipod.in_position for amphipod in self.amphipods.values()])

    def hallway_clear(self, amphipod, destination_x):
        left = min(amphipod.x, destination_x)
        right = max(amphipod.x, destination_x)
        return all(
            [
                (x, HALLWAY_ROW) not in self.amphipods
                for x in HALLWAY_COLUMNS
                if (left <= x <= right) and (x != amphipod.x)
            ]
        )


class Amphipod:
    def __init__(self, world, value, x, y):
        self.world = world
        self.value = value
        self.x = x
        self.y = y
        self.world += self

    def __str__(self):
        return self.value

    def distance(self, destination_x, destination_y):
        return abs(self.x - destination_x) + abs(self.y - destination_y)

    def move(self, destination_x, destination_y):
        steps = self.distance(destination_x, destination_y)
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

    @property
    def can_leave_room(self):
        column = [
            amphipod
            for amphipod in self.world.amphipods.values()
            if amphipod.x == self.x
        ]
        if all([amphipod.in_position for amphipod in column]):
            return False
        if min([amphipod.y for amphipod in column]) < self.y:
            return False
        return True

    def best_room_available(self):
        column = [
            amphipod
            for amphipod in self.world.amphipods.values()
            if amphipod.x == self.destination_column
        ]
        if any([not amphipod.in_position for amphipod in column]):
            return
        if column:
            y = min([amphipod.y for amphipod in column]) - 1
        else:
            y = 5
        yield (self.destination_column, y)

    def possible_moves(self):
        if self.in_hallway:
            if self.world.hallway_clear(self, self.destination_column):
                yield from self.best_room_available()
        elif self.can_leave_room:
            for x in HALLWAY_COLUMNS:
                if self.world.hallway_clear(self, x):
                    yield x, HALLWAY_ROW


test_world = World(
    lines=[
        "#############",
        "#...........#",
        "###.#.#.#.###",
        "  #.#.#.#.#  ",
        "  #########  ",
    ]
)

test_amphipod = Amphipod(world=test_world, value="A", x=5, y=3)
test_world += test_amphipod

assert test_amphipod.distance(4, 1) == 3
assert not test_amphipod.in_hallway
assert test_world.occupied(5, 3)

assert not test_world.occupied(2, 1)
test_amphipod.move(2, 1)
assert not test_world.occupied(5, 3)
assert test_world.occupied(2, 1)


def explore(world, cost):
    global min_cost
    world_string = str(world)
    if world_string in seen and cost >= seen[world_string]:
        return
    if min_cost and cost >= min_cost:
        return
    if world.complete:
        if min_cost is None or cost < min_cost:
            min_cost = cost
        yield cost
        return

    seen[world_string] = cost
    for amphipod in world.amphipods.values():
        original_amphipod = amphipod
        for move in amphipod.possible_moves():
            amphipod = deepcopy(original_amphipod)
            move_cost = amphipod.move(*move)
            yield from explore(amphipod.world, cost + move_cost)


seen = {}
min_cost = None
world = World(lines)
for cost in explore(world, 0):
    print(f"{cost}")
