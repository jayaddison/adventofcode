from itertools import permutations, product
from math import pow, sqrt


def parse_beacon(coordinates):
    x, y, z = coordinates.split(",")
    return (int(x), int(y), int(z))


class Scanner:
    def __init__(self, name, beacons):
        self.name = name
        self.beacons = set([parse_beacon(coordinates) for coordinates in beacons if coordinates.strip()])

    def __str__(self):
        return self.name


class KnowledgeBase:
    def __init__(self, scanner):
        self.beacons = scanner.beacons

    def transform(self, target, axis_mapping, axis_multiplication):
        return (
            target[axis_mapping[0]] * axis_multiplication[0],
            target[axis_mapping[1]] * axis_multiplication[1],
            target[axis_mapping[2]] * axis_multiplication[2],
        )

    def offset(self, source, target, axis_mapping, axis_multiplication):
        target = self.transform(target, axis_mapping, axis_multiplication)
        return (
            source[0] - target[0],
            source[1] - target[1],
            source[2] - target[2],
        )

    def determine_orientation(self, scanner):
        for axis_mapping in permutations([0, 1, 2]):  # (x, y, z) -> (x, y, z), (x, z, y), ...
            for axis_multiplication in product([-1, 1], repeat=3):
                for keystone_source in self.beacons:
                    for keystone_target in scanner.beacons:
                        keystone_offset = self.offset(
                            keystone_source,
                            keystone_target,
                            axis_mapping,
                            axis_multiplication,
                        )
                        comparison_sources = [beacon for beacon in self.beacons if beacon != keystone_source]
                        comparison_targets = [beacon for beacon in scanner.beacons if beacon != keystone_target]
                        matches = sum(
                            self.offset(
                                source,
                                target,
                                axis_mapping,
                                axis_multiplication,
                            ) == keystone_offset
                            for (source, target) in product(comparison_sources, comparison_targets)
                        )
                        if matches >= 3:
                            print(f"Determined VALID axis_mapping {axis_mapping} with multipliers {axis_multiplication} keystone {keystone_offset}")
                            return axis_mapping, axis_multiplication
        return None, None

    def import_beacons(self, beacons, axis_mapping, axis_multipliers):
        pass


orientations = open("19.txt").read()
blocks = orientations.split("\n\n")
scanners = set()
for block in blocks:
    readout = block.split("\n")
    name, beacons = readout[0], readout[1:]
    scanners.add(Scanner(name, beacons))

knowledgebase = KnowledgeBase(scanners.pop())
for scanner in scanners:
    axis_mapping, axis_multipliers = knowledgebase.determine_orientation(scanner)
    knowledgebase.import_beacons(scanner.beacons, axis_mapping, axis_multipliers)
