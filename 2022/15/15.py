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


def turn(direction_x, direction_y):
    match direction_x, direction_y:
        case (-1, 0):
            return (1, -1)
        case (1, 0):
            return (-1, 1)
        case (0, 1):
            return (-1, -1)
        case (0, -1):
            return (1, 1)


def boundary(entity_x, entity_y, entity_range):
    results = {}
    for direction_x, direction_y in (-1, 0), (1, 0), (0, 1), (0, -1):

        # Find the boundary point in each cardinal direction
        boundary_x, boundary_y = entity_x + direction_x, entity_y + direction_y
        while distance(entity_x, entity_y, boundary_x, boundary_y) <= entity_range:
            boundary_x += direction_x
            boundary_y += direction_y
        results[(boundary_x, boundary_y)] = turn(direction_x, direction_y)

    # Trace from each cardinal boundary point to the next
    for (boundary_x, boundary_y), (turn_x, turn_y) in results.items():
        yield boundary_x, boundary_y
        while (boundary_x + turn_x, boundary_y + turn_y) not in results:
            boundary_x += turn_x
            boundary_y += turn_y
            yield boundary_x, boundary_y


from collections import Counter

range_limit = int(input("What's the range limit?\n"))
boundary_counter = Counter()
for sensor, sensor_range in sensor_ranges.items():
    for boundary_position in boundary(*sensor, sensor_range):
        boundary_counter[boundary_position] += 1

candidates = Counter()
for (boundary_x, boundary_y), count in boundary_counter.items():
    if not 0 <= boundary_x <= range_limit:
        continue
    if not 0 <= boundary_y <= range_limit:
        continue
    position = boundary_x, boundary_y
    for sensor, sensor_range in sensor_ranges.items():
        if distance(*position, *sensor) <= sensor_range:
            break
    else:
        candidates[position] += count

(common_x, common_y), _ = boundary_counter.most_common(1)[0]
assert 0 <= common_x <= range_limit
assert 0 <= common_y <= range_limit
print(f"{common_x * range_limit + common_y}")

assert distance(2, 0, -2, 2) == 6
assert set(boundary(0, 0, 1)) == {
    ( 0,  2),
    (-1,  1),
    (-2,  0),
    (-1, -1),
    ( 0, -2),
    ( 1, -1),
    ( 2,  0),
    ( 1,  1),
    ( 0,  2),
}
