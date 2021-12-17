class Probe:

    def __init__(self, x=0, y=0, velocity_x=0, velocity_y=0):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
    
    def step(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_x += (1 if self.velocity_x < 0 else -1)
        self.velocity_y -= 1

    def is_below(self, target):
        return self.y < target.ymin


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

# Program
content = open("17.txt").read().strip()

p = Probe()
t = Target(content)

prev_x = p.x
while True:
    p.step()
    print(f"probe is at {p.x}, {p.y}")
    print(f"probe is within target: {t.contains(p)}")

    horizontally_stopped = p.x == prev_x
    horizontally_missed = not t.horizontally_contains(p)

    if p.is_below(t):
        print("probe fell below target")
        break
    if horizontally_stopped and horizontally_missed:
        print("probe stopped horizontally outside the target area")
        break
