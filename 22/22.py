class Cube:

    def __init__(self):
        self.xbounds = (-50, 50 + 1)
        self.ybounds = (-50, 50 + 1)
        self.zbounds = (-50, 50 + 1)
        self.cube = []
        for z in range(*self.zbounds):
            grid = []
            for y in range(*self.ybounds):
                row = []
                for x in range(*self.xbounds):
                    row.append(False)
                grid.append(row)
            self.cube.append(grid)

    def __len__(self):
        total = 0
        for z in range(*self.zbounds):
            for y in range(*self.ybounds):
                total += sum(self.cube[z][y])
        return total

    def apply_operation(self, instruction, xrange, yrange, zrange):
        xrange[0] = max(xrange[0], self.xbounds[0])
        xrange[1] = min(xrange[1], self.xbounds[1])
        yrange[0] = max(yrange[0], self.ybounds[0])
        yrange[1] = min(yrange[1], self.ybounds[1])
        zrange[0] = max(zrange[0], self.zbounds[0])
        zrange[1] = min(zrange[1], self.zbounds[1])

        for z in range(*zrange):
            for y in range(*yrange):
                for x in range(*xrange):
                    try:
                        self.cube[z][y][x] = instruction
                    except:
                        pass

def parse_range_string(text, expected_prefix):
    assert text.startswith(expected_prefix)
    text = text.removeprefix(expected_prefix)
    range = [int(value) for value in text.split("..")]
    range[-1] += 1
    return range


content = open("22.txt").read()
operations = []
for line in content.split("\n"):
    line = line.strip()
    if not line:
        continue
    instruction_string, range_strings = line.split(" ")
    instruction = instruction_string == "on"
    xrange_string, yrange_string, zrange_string = range_strings.split(",")
    xrange = parse_range_string(xrange_string, "x=")
    yrange = parse_range_string(yrange_string, "y=")
    zrange = parse_range_string(zrange_string, "z=")
    operations.append((instruction, xrange, yrange, zrange))

cube = Cube()
for operation in operations:
    cube.apply_operation(*operation)
print(len(cube))
