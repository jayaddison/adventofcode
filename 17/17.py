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

max_y = 0
for velocity_x in range(0, 50):
    for velocity_y in range(0, 1000):
        p = Probe(velocity_x=velocity_x, velocity_y=velocity_y)
        hit, steps = p.finds_target(t)
        if hit:
            max_y = max(max_y, p.max_y)
            if p.max_y == max_y:
                print(f"{velocity_x},{velocity_y}")

# Answer validation
p = Probe(velocity_x=15, velocity_y=76)
hit, _ = p.finds_target(t)
assert hit

print(max_y)
