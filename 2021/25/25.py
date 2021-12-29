def char_to_direction(char):
    if char == ">":
        return (1, 0)
    if char == "v":
        return (0, 1)


class Cucumber:
    def __init__(self, world, x, y, char):
        self.world = world
        self.x = x
        self.y = y
        self.char = char
        self.direction = char_to_direction(char)
        self.world += self

    def __str__(self):
        return self.char

    @property
    def current_coordinates(self):
        return self.x, self.y

    @property
    def next_coordinates(self):
        x, y = self.current_coordinates
        step_x, step_y = self.direction
        next_x, next_y = (x + step_x, y + step_y)
        return (
            (next_x if next_x < self.world.width else 0),
            (next_y if next_y < self.world.height else 0),
        )

    @property
    def blocked(self):
        return self.world.occupied(*self.next_coordinates)

    def step(self):
        del self.world.grid[self.current_coordinates]
        self.world.grid[self.next_coordinates] = self
        self.x, self.y = self.next_coordinates


class Herd:
    def __init__(self, direction):
        self.direction = direction
        self.cucumbers = set()
        self.frontier = set()

    def __add__(self, cucumber):
        self.cucumbers.add(cucumber)
        return self

    def step(self):
        self.update_frontier()
        for cucumber in self.frontier:
            cucumber.step()

    def update_frontier(self):
        self.frontier.clear()
        for cucumber in self.cucumbers:
            if not cucumber.blocked:
                self.frontier.add(cucumber)


class World:
    def __init__(self, text):
        self.grid = {}
        self.herds = {}
        self.width = 0
        self.height = 0
        self._load_state(text)

    def _load_state(self, text):
        for y, line in enumerate(text.strip().split("\n")):
            line = line.strip()
            if not line:
                continue
            for x, char in enumerate(line):
                if char == ".":
                    continue
                cucumber = Cucumber(self, x, y, char)

    def __add__(self, cucumber):
        coordinates = (cucumber.x, cucumber.y)
        direction = cucumber.direction
        if direction not in self.herds:
            self.herds[direction] = Herd(direction)
        self.grid[coordinates] = cucumber
        self.herds[direction] += cucumber
        self.width = max(self.width, cucumber.x + 1)
        self.height = max(self.height, cucumber.y + 1)
        return self

    def __str__(self):
        result = []
        for y in range(self.height):
            for x in range(self.width):
                char = str(self.grid.get((x, y), "."))
                result.append(char)
            result.append("\n")
        return str().join(result)

    def occupied(self, x, y):
        return (x, y) in self.grid

    def step(self):
        herd_directions = [
            char_to_direction(">"),
            char_to_direction("v"),
        ]
        for direction in herd_directions:
            self.herds[direction].step()


test_world = World(
    text="""
...>...
.......
......>
v.....>
......>
.......
..vvv..
"""
)

print(test_world)
for _ in range(4):
    test_world.step()
    print(test_world)

assert (
    str(test_world).strip()
    == """
>......
..v....
..>.v..
.>.v...
...>...
.......
v......
""".strip()
)

content = open("25.txt").read()
world = World(content)

n = 0
while n == 0 or any([herd.frontier for herd in world.herds.values()]):
    world.step()
    n += 1
print(n)
