def triangle(n):
    result = n
    while n:
        n -= 1
        result += n
    return result

class Probe:

    def __init__(self, x=0, y=0, velocity_x=0, velocity_y=0):
        self.x = x
        self.y = y
        self.max_y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def step(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.max_y = max(self.max_y, self.y)
        if self.velocity_x != 0:
            self.velocity_x += (1 if self.velocity_x < 0 else -1)
        self.velocity_y -= 1

    def is_below(self, target):
        return self.y < target.ymin

    def finds_target_horizontally(self, target):
        prev_x = self.x
        steps = 0

        while True:
            self.step()
            steps += 1

            if target.horizontally_contains(self):
                return True, steps

            horizontally_stopped = self.x == prev_x
            horizontally_missed = not target.horizontally_contains(self)

            if horizontally_stopped and horizontally_missed:
                break
            prev_x = self.x

        return False, steps

    def finds_target(self, target):
        prev_x = self.x
        steps = 0

        while True:
            self.step()
            steps += 1

            if target.contains(self):
                return True, steps

            horizontally_stopped = self.x == prev_x
            horizontally_missed = not target.horizontally_contains(self)

            if self.is_below(target):
                break
            if horizontally_stopped and horizontally_missed:
                break
            prev_x = self.x

        return False, steps

    def candidate_x_velocities(self, target):
        for target_x in range(target.xmin, target.xmax):
            range_start = min(0, target_x + 1)
            range_end = max(0, target_x + 1)
            for velocity in range(range_start, range_end):
                p = Probe(velocity_x=velocity)
                hit, steps = p.finds_target_horizontally(target)
                if hit:
                    yield velocity, steps

    def candidate_y_velocities(self, target, expected_steps):
        expected_drop = triangle(expected_steps)
        for target_y in range(target.ymin, target.ymax):
            yield target_y + expected_drop


class Target:

    def _parse_range(self, text):
        axis, range = text.split("=")
        min_val, max_val = range.split("..")
        return int(min_val), int(max_val)

    def _parse_coordinates(self, text):
        preamble, coordinates = text.split(":")
        xrange, yrange = coordinates.strip().split(",")
        xmin, xmax = self._parse_range(xrange.strip())
        ymin, ymax = self._parse_range(yrange.strip())
        return xmin, xmax, ymin, ymax

    def __init__(self, text):
        xmin, xmax, ymin, ymax = self._parse_coordinates(text)
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    def horizontally_contains(self, probe):
        return self.xmin <= probe.x <= self.xmax

    def vertically_contains(self, probe):
        return self.ymin <= probe.y <= self.ymax

    def contains(self, probe):
        within_x = self.horizontally_contains(probe)
        within_y = self.vertically_contains(probe)
        return within_x and within_y

# Tests
p = Probe(x=25, y=-7)
t = Target("target area: x=20..30, y=-10..-5")

assert t.contains(p)

p = Probe(x=10, y=10)
t = Target("target area: x=10..20, y=11..20")

assert t.horizontally_contains(p)
assert p.is_below(t)

assert triangle(3) == 6
assert triangle(6) == 21

# Program
content = open("17.txt").read().strip()

t = Target(content)

p = Probe()
max_y = 0
for velocity_x, expected_steps in p.candidate_x_velocities(t):
    for velocity_y in p.candidate_y_velocities(t, expected_steps):
        p = Probe(velocity_x=velocity_x, velocity_y=velocity_y)
        hit, steps = p.finds_target(t)
        max_y = max(max_y, p.max_y) if hit else max_y

print(max_y)
