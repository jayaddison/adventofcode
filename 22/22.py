def extent_size(extent):
    xbounds, ybounds, zbounds = extent
    return (
        (xbounds[1] - xbounds[0])
        * (ybounds[1] - ybounds[0])
        * (zbounds[1] - zbounds[0])
    )


def constrain(input, bounds):
    result = []
    for index, _ in enumerate(input):
        result.append(
            (
                max(input[index][0], bounds[index][0]),
                min(input[index][1], bounds[index][1]),
            )
        )
    return tuple(result)


assert constrain(input=((-5, 5),), bounds=((-1, 10),)) == ((-1, 5),)


class Cube:
    def __init__(self, xbounds, ybounds, zbounds):
        self.xbounds = xbounds
        self.ybounds = ybounds
        self.zbounds = zbounds
        self.subtractions = []

    def size(self):
        return extent_size((self.xbounds, self.ybounds, self.zbounds))

    def size(self):
        return extent_size((self.xbounds, self.ybounds, self.zbounds))

    def __str__(self):
        return f"({self.xbounds},{self.ybounds},{self.zbounds}) = {self.size()}"

    def intersection(self, cube):
        bounds = constrain(
            (cube.xbounds, cube.ybounds, cube.zbounds),
            (self.xbounds, self.ybounds, self.zbounds),
        )
        xintersect, yintersect, zintersect = bounds
        return Cube(xintersect, yintersect, zintersect)

    def subtract(self, cube):
        intersection = self.intersection(cube)
        if not intersection.size():
            return 0
        subtracted = 0
        for subtraction in self.subtractions:
            subtracted += subtraction.subtract(intersection)
        self.subtractions.append(intersection)
        return intersection.size() - subtracted


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


cubes = []
measurement_area = Cube((-50, 51), (-50, 51), (-50, 51))
total = 0
for instruction, xrange, yrange, zrange in operations:
    operation_cube = Cube(xrange, yrange, zrange)
    operation_cube = measurement_area.intersection(operation_cube)
    print(f"processing {operation_cube}")
    if instruction:
        added = operation_cube.size()
        total += added

    for cube in cubes:
        subtracted = cube.subtract(operation_cube)
        total -= subtracted

    if instruction:
        cubes.append(operation_cube)

print(total)
