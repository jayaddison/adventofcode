content = open("15.txt").read()


def parse_coords(location):
    x_fragment, y_fragment = location.split(", ")
    yield int(x_fragment[2:])
    yield int(y_fragment[2:])


def parse_sensor_line(line):
    sensor_info, beacon_info = line.split(":")
    yield from parse_coords(sensor_info[10:])
    yield from parse_coords(beacon_info[22:])


def distance(x, y, other_x, other_y):
    return abs(x - other_x) + abs(y - other_y)


def nearest_beacon(x, y):
    global beacons
    nearest, nearest_distance = None, None
    for beacon_x, beacon_y in beacons:
        beacon_distance = distance(beacon_x, beacon_y, x, y)
        if nearest is None or beacon_distance < nearest_distance:
            nearest = beacon_x, beacon_y
            nearest_distance = beacon_distance
    return nearest


# Collect sensor and beacon locations, and determine map extents
min_x, min_y, max_x, max_y = 0, 0, 0, 0
sensors, beacons = set(), set()
for line in content.splitlines():
    sensor_x, sensor_y, beacon_x, beacon_y = parse_sensor_line(line)
    sensors.add((sensor_x, sensor_y))
    beacons.add((beacon_x, beacon_y))
    min_x, min_y, max_x, max_y = (
        min(min_x, sensor_x, beacon_x),
        min(min_y, sensor_y, beacon_y),
        max(max_x, sensor_x, beacon_x),
        max(max_y, sensor_y, beacon_y),
    )


# Determine the range of each sensor
sensor_ranges = {
    sensor: distance(*sensor, *nearest_beacon(*sensor)) for sensor in sensors
}


# Produce a map of the surroundings
for y in range(min_y - 1, max_y + 2):
    for x in range(min_x - 1, max_x + 2):
        is_beacon = (x, y) in beacons
        is_sensor = (x, y) in sensors
        symbol = "."
        for sensor, sensor_range in sensor_ranges.items():
            if distance(x, y, *sensor) <= sensor_range:
                symbol = "#"
                break
        symbol = "B" if is_beacon else "S" if is_sensor else symbol
        print(symbol, end="")
    print()


Y = 10
within_range = 0
max_range = max(v for k, v in sensor_ranges.items()) + 1
for x in range(min_x - max_range, max_x + max_range):
    position = x, Y
    for sensor, sensor_range in sensor_ranges.items():
        if position in beacons or position in sensors:
            continue
        if distance(*position, *sensor) <= sensor_range:
            within_range += 1
            break
print(within_range)


assert distance(2, 0, -2, 2) == 6
