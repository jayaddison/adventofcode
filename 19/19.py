from collections import defaultdict
from itertools import permutations
import json
from math import pow, sqrt


class Beacon:

    def __init__(self, coordinates):
        x, y, z = coordinates.split(",")
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    def __str__(self):
        return f"{self.x},{self.y},{self.z}"

    def distance(self, beacon):
        x_sq_dist = pow(beacon.x - self.x, 2)
        y_sq_dist = pow(beacon.y - self.y, 2)
        z_sq_dist = pow(beacon.z - self.z, 2)
        return sqrt(x_sq_dist + y_sq_dist + z_sq_dist)


class Scanner:

    def __init__(self, name, beacons):
        self.name = name
        self.beacons = [Beacon(beacon) for beacon in beacons if beacon.strip()]
        self.beacon_numbers = {beacon: index for index, beacon in enumerate(self.beacons)}

    def observed_distances(self):
        unsorted_distances = defaultdict(lambda: list)
        for beacon_a, beacon_b in permutations(self.beacons, 2):
            distance = beacon_a.distance(beacon_b)
            unsorted_distances[distance] = (self.beacon_numbers[beacon_a], self.beacon_numbers[beacon_b])

        sorted_keys = sorted(unsorted_distances.keys())
        sorted_distances = {}
        for key in sorted_keys:
            sorted_distances[key] = unsorted_distances[key]
        return sorted_distances


test_orientations = open("different-orientations.txt").read()
test_blocks = test_orientations.split("\n\n")
for test_block in test_blocks:
    test_readout = test_block.split("\n")
    test_name, test_beacons = test_readout[0], test_readout[1:]
    test_scanner = Scanner(test_name, test_beacons)
