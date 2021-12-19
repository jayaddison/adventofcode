import heapq
from itertools import permutations, product
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
        print(f"Building initial knowledgebase from {scanner}")
        self.known_beacons = {beacon: beacon.fingerprint() for beacon in scanner.beacons}

        # Set the criteria by which concurrences are determined
        self.match_level = max(len(fingerprint) for fingerprint in self.known_beacons.values())

    def find_concurrences(self, scanner):
        print(f"Checking for {scanner} concurrences at match level {self.match_level}")

        concurrences = []
        for beacon in scanner.beacons:
            for known_beacon, known_fingerprint in self.known_beacons.items():
                concurrences.append((known_beacon, beacon))

        print(f"Found {len(concurrences)} beacons with concurrent fingerprints")
        if len(concurrences) > 12:
            return concurrences[:12]
        return []

    def transformed_offsets(self, concurrence, axis_mapping, axis_multiplication):
        source_beacon, target_beacon = concurrence
        source_beacon = (source_beacon.x, source_beacon.y, source_beacon.z)
        target_beacon = (target_beacon.x, target_beacon.y, target_beacon.z)
        target_beacon = (
            target_beacon[axis_mapping[0]] * axis_multiplication[0],
            target_beacon[axis_mapping[1]] * axis_multiplication[1],
            target_beacon[axis_mapping[2]] * axis_multiplication[2],
        )
        return (
            source_beacon[0] - target_beacon[0],
            source_beacon[1] - target_beacon[1],
            source_beacon[2] - target_beacon[2],
        )

    def determine_orientation(self, concurrences):
        if len(concurrences) < 12:
            print(
                f"Not supplied enough concurrences to determine orientation; 12 are required and {len(concurrences)} were provided"
            )
            return None, None

        result = None, None
        for axis_mapping in permutations([0, 1, 2]):  # (x, y, z) -> (x, y, z), (x, z, y), ...
            for axis_multiplication in product([-1, 1], repeat=3):
                sample_concurrence = concurrences[0]
                sample_offsets = self.transformed_offsets(
                    sample_concurrence, axis_mapping, axis_multiplication
                )

                if all(
                    self.transformed_offsets(concurrence, axis_mapping, axis_multiplication)
                    == sample_offsets
                    for concurrence in concurrences[1:]
                ):
                    print(f"Determined VALID axis_mapping {axis_mapping} with multipliers {axis_multiplication}")
                    result = axis_mapping, axis_multiplication
                else:
                    print(f"Found INVALID axis mapping {axis_mapping} with multipliers {axis_multiplication}")
        return result


orientations = open("19.txt").read()
blocks = orientations.split("\n\n")
scanners = set()
for block in blocks:
    readout = block.split("\n")
    name, beacons = readout[0], readout[1:]
    scanners.add(Scanner(name, beacons))

knowledgebase = KnowledgeBase(scanners.pop())
for scanner in scanners:
    concurrences = knowledgebase.find_concurrences(scanner)
    axis_mapping, axis_multipliers = knowledgebase.determine_orientation(concurrences)
