from collections import defaultdict
import heapq
from itertools import permutations
from math import pow, sqrt


class Beacon:

    def __init__(self, coordinates):
        x, y, z = coordinates.split(",")
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.reference_distances = []

    def __str__(self):
        return f"{self.x},{self.y},{self.z}"

    def distance(self, beacon):
        x_sq_dist = pow(beacon.x - self.x, 2)
        y_sq_dist = pow(beacon.y - self.y, 2)
        z_sq_dist = pow(beacon.z - self.z, 2)
        return sqrt(x_sq_dist + y_sq_dist + z_sq_dist)

    def chart_reference_beacon(self, beacon):
        distance = self.distance(beacon)
        if len(self.reference_distances) == 10:
            heapq.heappushpop(self.reference_distances, distance)
        else:
            heapq.heappush(self.reference_distances, distance)

    def fingerprint(self):
        return set(self.reference_distances)


class Scanner:

    def __init__(self, name, beacons):
        self.name = name
        self.beacons = [Beacon(beacon) for beacon in beacons if beacon.strip()]
        for beacon_a, beacon_b in permutations(self.beacons, 2):
            beacon_a.chart_reference_beacon(beacon_b)

    def __str__(self):
        return self.name


class KnowledgeBase:

    def __init__(self, scanner):
        # beacon -> fingerprint mapping
        self.known_beacons = {}

        print(f"Building initial knowledgebase from {scanner}")
        for beacon in scanner.beacons:
            self.known_beacons[beacon] = beacon.fingerprint()

        # Set the criteria by which concurrences are determined
        self.match_level = max(len(fingerprint) for fingerprint in self.known_beacons.values())

    def find_concurrences(self, scanner):
        print(f"Checking for {scanner} concurrences at match level {self.match_level}")

        match_count = 0
        concurrences = []
        for beacon in scanner.beacons:
            fingerprint = beacon.fingerprint()
            if len(fingerprint) < self.match_level:
                continue
            for known_beacon, known_fingerprint in self.known_beacons.items():
                if known_fingerprint == fingerprint:
                    concurrences.append((known_beacon, beacon))
                    break

        print(f"Found {len(concurrences)} beacons with concurrent fingerprints")


test_orientations = open("different-orientations.txt").read()
test_blocks = test_orientations.split("\n\n")
test_scanners = set()
for test_block in test_blocks:
    test_readout = test_block.split("\n")
    test_name, test_beacons = test_readout[0], test_readout[1:]
    test_scanners.add(Scanner(test_name, test_beacons))

test_knowledgebase = None
for test_scanner in test_scanners:
    if test_knowledgebase is None:
        test_knowledgebase = KnowledgeBase(test_scanner)
    else:
        test_knowledgebase.find_concurrences(test_scanner)
